# How to Get Your Cursor Cloud Agent API Key

## Step 1 — Generate API Key

1. Open **https://cursor.com/dashboard**
2. Log in with your Cursor account
3. Click the **Integrations** tab
4. Click **Generate API Key**
5. Copy the generated key

> Note: You need an active Cursor account with a Trial or Paid plan, and usage-based pricing must be enabled.

## Step 2 — Connect GitHub

If you haven't already:
1. In the Cursor Dashboard, go to **Settings** or **Integrations**
2. Connect your **GitHub** (or GitLab) account
3. Grant read-write permissions to the repos you want agents to work on

## Step 3 — Save API Key

```bash
# Method A — File (recommended)
echo 'your_api_key_here' > ~/.cursor_api_key
chmod 600 ~/.cursor_api_key

# Method B — Environment variable
export CURSOR_API_KEY='your_api_key_here'
# Add to ~/.bashrc or ~/.zshrc for persistence
```

## Step 4 — Verify

```bash
python3 ~/.openclaw/workspace/skills/cursor-agent/scripts/cursor_bga.py models
```

If successful, you'll see a list of available models.

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Invalid or expired API key | Re-generate key in Dashboard |
| 403 Forbidden | Plan doesn't support Cloud Agents | Upgrade plan or enable usage-based pricing |
| 429 Rate Limited | Too many requests | Wait and retry (repos endpoint: 1/min, 30/hr) |

## API Documentation

Official docs: https://cursor.com/docs/cloud-agent/api/endpoints
