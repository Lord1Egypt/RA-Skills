# Service Tokens — Programmatic Access Through Cloudflare Access

Use when an app, CLI, or native client needs to connect to an agent without going through a
browser-based login flow.

## How Service Tokens Work

```
App / CLI
  │  sends headers:
  │    CF-Access-Client-Id: <id>.access
  │    CF-Access-Client-Secret: <secret>
  ↓
Cloudflare Edge
  └── Validates token → allows through to Cloudflare Tunnel
        ↓
      localhost:18789  (OpenClaw gateway)
```

Tokens are permanent until rotated. No JWT expiry, no browser redirect.

---

## Creating a Service Token

1. **Zero Trust → Access → Service Auth → Service Tokens → Create Service Token**
2. Name it descriptively: `OpenClaw CLI - Charles laptop`, `iOS App - Koda`
3. Set **Token Duration**: `Non-expiring` for permanent apps, or a date for time-limited access
4. Copy **both** values immediately — the secret is only shown once

---

## Attaching the Token to an Application

The Access Application needs a policy that accepts this service token:

1. **Zero Trust → Access → Applications → [your app] → Edit**
2. **Policies tab → Add a policy** (separate from the human login policy)
3. Policy settings:
   - **Policy name:** `Service Token Access`
   - **Action:** Allow
   - **Include:** Service Token → select the token you created
4. Save

The application now accepts **either** human login OR the service token.

---

## Usage Examples

### curl / REST API
```bash
CF_ID="your-client-id.access"
CF_SECRET="your-client-secret"

curl -H "CF-Access-Client-Id: $CF_ID" \
     -H "CF-Access-Client-Secret: $CF_SECRET" \
     https://koda.teamplayers.ai/api/health
```

### WebSocket (Node.js)
```javascript
const ws = new WebSocket("wss://koda.teamplayers.ai", {
  headers: {
    "CF-Access-Client-Id": process.env.CF_CLIENT_ID,
    "CF-Access-Client-Secret": process.env.CF_CLIENT_SECRET,
  },
});
```

### OpenClaw CLI remote connection (`openclaw.json`)
```json
{
  "gateway": {
    "remote": {
      "url": "wss://koda.teamplayers.ai",
      "token": "<openclaw-gateway-token>",
      "headers": {
        "CF-Access-Client-Id": "<id>.access",
        "CF-Access-Client-Secret": "<secret>"
      }
    }
  }
}
```

---

## Security Notes

- Treat service tokens like API keys — store in vault, never commit to git
- Create one token per client/device (granular revocation)
- Revoke immediately if a device is lost: **Zero Trust → Service Auth → Revoke**
- For CLI tools, store in `~/.openclaw/secrets.json` and reference via SecretRef

---

## Rotating a Service Token

1. Create a new token (keep the old one active during transition)
2. Update all clients to use the new token
3. Revoke the old token once all clients are confirmed updated

Cloudflare logs all service token usage in **Zero Trust → Logs → Access** — use this to confirm no remaining clients are using the old token before revoking.
