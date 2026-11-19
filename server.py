from flask import Flask, request, jsonify
import secrets
import time

app = Flask(__name__)
invites = {}

@app.get("/")
def home():
    return "MyAndroidApp server is running"

@app.post("/invite")
def create_invite():
    token = secrets.token_urlsafe(32)
    invites[token] = {
        "created": time.time(),
        "approved": False,
        "used": False
    }
    return jsonify({
        "invite": request.host_url + "join/" + token
    })

@app.get("/join/<token>")
def join(token):
    invite = invites.get(token)
    if not invite or invite["used"] or time.time() - invite["created"] > 600:
        return "Invite expired or invalid", 404
    return """
    <h2>MyAndroidApp</h2>
    <p>ఈ పరికరాన్ని కనెక్ట్ చేయడానికి అనుమతిస్తున్నారా?</p>
    <form method="post" action="/approve/""" + token + """">
    <button type="submit">Approve Connection</button>
    </form>
    """

@app.post("/approve/<token>")
def approve(token):
    invite = invites.get(token)
    if not invite or invite["used"] or time.time() - invite["created"] > 600:
        return "Invite expired or invalid", 404
    invite["approved"] = True
    invite["used"] = True
    return "Connection approved. You may close this page."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
