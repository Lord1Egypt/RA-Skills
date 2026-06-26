# Agents Mail — Common Patterns (v0.4)

## Pattern 1: Get Mailbox and Send (Zero Setup)

```python
import requests, os

# One call — no sign-up, no API key needed
agent = requests.post("https://agentsmail.org/api/getemailaddress",
    json={"agent_name": "inbox-watcher"}).json()

# Store securely as environment variable (NOT in plaintext files)
# os.environ["AGENTSMAIL_API_KEY"] = agent["api_key"]
api_key = agent["api_key"]

print(f"Email: {agent['email']}")

# Send immediately — 10 free sends at Tier 0
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
result = requests.post("https://agentsmail.org/api/send",
    headers=headers,
    json={
        "to": "owner@example.com",
        "subject": "Hello from my agent",
        "text": "I just got my own email address!"
    }).json()

print(f"Sent! Remaining: {result['trial_sends']['remaining']}")
```

## Pattern 2: Check Inbox

```python
import requests

api_key = os.environ.get("AGENTSMAIL_API_KEY")
headers = {"Authorization": f"Bearer {api_key}"}

# Check for unread emails
emails = requests.get("https://agentsmail.org/api/inbox?is_read=0",
    headers=headers).json()

for email in emails.get("emails", []):
    print(f"From: {email['from']}, Subject: {email['subject']}")
```

## Pattern 3: Auto-Responder

Poll inbox and reply to new messages:

```python
import requests, time, os

API = "https://agentsmail.org/api"
api_key = os.environ.get("AGENTSMAIL_API_KEY")
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

while True:
    emails = requests.get(f"{API}/inbox?is_read=0", headers=headers).json()

    for email in emails.get("emails", []):
        # Read the full email (auto-marks as read)
        detail = requests.get(f"{API}/inbox/{email['email_id']}", headers=headers).json()

        # Reply
        requests.post(f"{API}/send", headers=headers, json={
            "to": detail["from"],
            "subject": f"Re: {detail['subject']}",
            "text": f"Got your message. Processing now."
        })

    time.sleep(30)
```

## Pattern 4: Upgrade to Permanent Mailbox

```python
import requests, os

api_key = os.environ.get("AGENTSMAIL_API_KEY")
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

# Upgrade — owner gets magic link, click to confirm
result = requests.post("https://agentsmail.org/api/upgrade",
    headers=headers,
    json={
        "owner_email": "owner@example.com",
        "name": "my-agent"
    }).json()

print(f"Future email: {result['future_email']}")
# → my-agent@agentsmail.org (after owner confirms)
```

## Pattern 5: Webhook-Driven Pipeline (Tier 1+)

```python
import requests, os

api_key = os.environ.get("AGENTSMAIL_API_KEY")
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

# Register webhook (must be public HTTPS)
webhook = requests.post("https://agentsmail.org/api/webhooks",
    headers=headers,
    json={
        "url": "https://your-server.com/incoming-email",
        "events": ["email.received"]
    }).json()

print(f"Webhook secret: {webhook['secret']}")  # For HMAC verification
```

Handle incoming webhooks:

```python
from flask import Flask, request
import hmac, hashlib

app = Flask(__name__)
WEBHOOK_SECRET = os.environ.get("AGENTSMAIL_WEBHOOK_SECRET")

@app.route("/incoming-email", methods=["POST"])
def handle():
    sig = request.headers.get("X-Webhook-Signature", "")
    expected = hmac.new(WEBHOOK_SECRET.encode(), request.data, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(sig, expected):
        return "Bad signature", 401

    email = request.json
    print(f"New email from {email['from']}: {email['subject']}")
    return "OK"
```

## Pattern 6: HEARTBEAT.md (Recommended for OpenClaw / Local Agents)

For agents without a public server, add inbox checking to your HEARTBEAT.md:

```markdown
## Check AgentsMail Inbox

curl -s https://agentsmail.org/api/inbox?is_read=0 \
  -H "Authorization: Bearer $AGENTSMAIL_API_KEY"

If there are unread emails, summarize them (sender, subject, preview).
If no unread emails, reply HEARTBEAT_OK.
```

This automatically checks your inbox on each heartbeat cycle (typically every 30 minutes) and notifies your owner when new emails arrive.

## Pattern 7: Access Control (Tier 1+)

```python
import requests, os

api_key = os.environ.get("AGENTSMAIL_API_KEY")
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

# Whitelist trusted senders
requests.post("https://agentsmail.org/api/acl", headers=headers,
    json={"email": "boss@company.com", "type": "whitelist"})

# Blacklist spam
requests.post("https://agentsmail.org/api/acl", headers=headers,
    json={"email": "spammer@evil.com", "type": "blacklist"})
```
