# Authentication (OpenClaw / mcporter)

Axiom uses OAuth 2.0 with PKCE. On OpenClaw, `mcporter` (≥0.8.0) handles the OAuth token lifecycle.

The auth flow uses a **device-flow pattern**: mcporter opens an authorization page, that page displays an activation URL, and the user approves on their own device (phone, laptop, etc.). The agent never sees credentials directly.

## Prerequisites

- `mcporter` ≥0.8.0 on PATH (check with `mcporter --version`)
- A headless browser CLI for reading the activation URL from the rendered page:
  - **Recommended:** `agent-browser` (Rust native, fast, no Python needed): `npm install -g agent-browser && agent-browser install`
  - **Alternative:** `browser-use` (Python): `uv add browser-use`
- Axiom registered as a server: `mcporter config add axiom --url https://mcp.useaxiom.ai/mcp`

## Auth Flow (step by step)

### Step 1: Start mcporter auth in the background

```bash
mcporter auth axiom --reset --oauth-timeout 300000 --log-level info
```

Run this in the background. mcporter will:
1. Discover the authorization endpoint from Axiom's OAuth metadata
2. Start a local callback listener on a random port
3. Open the system browser to the authorization page
4. Print the OAuth authorize URL to stdout (at `info` log level)

The output will include a line like:

```
[mcporter] If the browser did not open, visit https://api.useaxiom.ai/api/auth/oauth2/authorize?response_type=code&client_id=ABC123&... manually.
```

Parse the URL from this log line. You'll navigate to it in the next step.

### Step 2: Navigate to the OAuth page in a headless browser

Open the OAuth authorize URL in a headless browser.

**Using agent-browser (recommended):**

```bash
agent-browser open "<OAUTH_AUTHORIZE_URL>"
sleep 2
```

**Using browser-use:**

```bash
browser-use open "<OAUTH_AUTHORIZE_URL>"
sleep 2
```

> **Note:** The `sleep 2` is important. The page needs time to hydrate before the activation URL element is available in the DOM.

> **Important:** The OAuth authorize URL is NOT the activation URL. Do not send the authorize URL to the user.

### Step 3: Find the activation URL

The page will show one of two states:

**Device flow (what you want):**
```
AI-powered wallet and payments

Sign in on another device
Open this link on your phone or another device to sign in

Activation URL
https://app.useaxiom.ai/oauth/activate?session=5fef9e2f-5a41-4a6a-8533-4e91076bd123
Waiting for authentication...
Expires in 4:57

Sign in directly instead
```

**Direct sign-in form (click through to device flow):**
If the page shows an email/password form instead, click the "Sign in on another device" button:

```bash
# agent-browser
agent-browser click "Sign in on another device"

# browser-use
browser-use click "Sign in on another device"
sleep 2
```

Then extract the activation URL:

```bash
# agent-browser
agent-browser eval "document.querySelector('a[href*=\"activate\"]')?.href"

# browser-use
browser-use eval "document.querySelector('a[href*=\"activate\"]')?.href"
```

The activation URL looks like:

```
https://app.useaxiom.ai/oauth/activate?session=5fef9e2f-5a41-4a6a-8533-4e91076bd123
```

### Understanding the two URLs

| URL | Example | Purpose | Who uses it |
|-----|---------|---------|-------------|
| OAuth authorize URL | `https://api.useaxiom.ai/api/auth/oauth2/authorize?client_id=...` | Starts the OAuth flow, renders the auth page | Agent (headless browser) |
| Activation URL | `https://app.useaxiom.ai/oauth/activate?session=...` | Approval link for the user | User (phone/device) |

Never send the OAuth authorize URL to the user. Always send the activation URL.

### Step 4: Send the activation URL to the user

Send only the activation URL:

> To connect Axiom Wallet, open this link on your phone and approve access:
> https://app.useaxiom.ai/oauth/activate?session=5fef9e2f-...

### Step 5: Wait for approval

The authorization page polls automatically. When the user approves:
1. The page redirects to mcporter's local callback (`127.0.0.1:<port>/callback`)
2. mcporter exchanges the authorization code for tokens
3. Tokens are stored persistently by mcporter
4. Authentication is complete

### Step 6: Clean up

Close the agent-browser session:

```bash
agent-browser close
```

### Step 7: Verify

```bash
mcporter call axiom.get_payment_method
```

Returns saved-card status and brand/last4 metadata if auth succeeded.

## Token Lifecycle

- Tokens are stored by mcporter and refreshed automatically on subsequent calls.
- If a token expires and cannot be refreshed, re-run `mcporter auth axiom`.
- To clear cached tokens and start fresh: `mcporter auth axiom --reset`

## Troubleshooting

### Activation URL not visible

If the page shows a login form, look for "Sign in on another device" and click it to switch to device-flow mode.

### Session expired (5-minute TTL)

The activation URL expires after 5 minutes. The page shows a "Try again" button. Click it to generate a fresh URL and resend to the user.

### mcporter says "Unknown MCP server 'axiom'"

Register Axiom first: `mcporter config add axiom --url https://mcp.useaxiom.ai/mcp`

Run mcporter from the directory containing `config/mcporter.json` (usually the OpenClaw workspace).

### OAuth authorize URL not in mcporter output

Make sure you're using `--log-level info`. At the default log level (`warn`), mcporter does not print the URL. If you still can't see it, intercept the system `open` command:

```bash
mkdir -p /tmp/fakebin
cat > /tmp/fakebin/open << 'EOF'
#!/bin/bash
echo "$@" >> /tmp/axiom-auth-url.txt
/usr/bin/open "$@"
EOF
chmod +x /tmp/fakebin/open

PATH=/tmp/fakebin:$PATH mcporter auth axiom --reset --oauth-timeout 300000 &
sleep 5
cat /tmp/axiom-auth-url.txt
```

Then navigate to the captured URL with `agent-browser open "<URL>"` (or `browser-use open "<URL>"`) and continue from Step 2.

### OAuth callback port mismatch

mcporter uses a random port for each auth attempt. Old URLs from previous attempts will not work. Always start a fresh `mcporter auth` rather than reusing old URLs.

### "Authorization successful" but mcporter still waiting

The page completed but mcporter didn't receive the callback. Kill mcporter and start a fresh auth flow.

### No headless browser available

Install one of these:
1. **agent-browser (recommended):** `npm install -g agent-browser && agent-browser install`
2. **browser-use:** `uv add browser-use`

Without a headless browser, the fallback is to run `mcporter auth axiom` and complete sign-in in the system browser that opens (requires a display).

## Security

- Never read, print, or share OAuth tokens, cookies, or browser state.
- Only share the activation URL with the user — nothing else from the page.
- Do not use `--verbose` / `-v` in agent sessions (can expose sensitive headers).
