---
name: openclaw-deal-scout
description: Autonomous Gmail-to-CRM deal pipeline for solo operators. Classifies inbound deal emails with Gemini, logs them to a free HubSpot CRM, notifies on Discord, and sends approved replies during UK business hours. Zero hosted infrastructure — runs as a single local MCP gateway.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env: ["GMAIL_CREDENTIALS_PATH", "GEMINI_API_KEY", "HUBSPOT_PRIVATE_APP_TOKEN"]
      anyBins: ["python3", "python"]
    primaryEnv: GEMINI_API_KEY
    envVars:
      - name: GMAIL_CREDENTIALS_PATH
        required: true
        description: Path to the OAuth client credentials JSON from Google Cloud Console (Gmail read + send scopes).
      - name: GEMINI_API_KEY
        required: true
        description: Gemini API key (Google AI Studio free tier) used for deal-vs-noise classification.
      - name: HUBSPOT_PRIVATE_APP_TOKEN
        required: true
        description: HubSpot Private App token (Settings -> Integrations -> Private Apps), free CRM tier.
      - name: NOTIFIER
        required: false
        description: Notification adapter selector — set to "discord" to enable alerts (default noop).
      - name: DISCORD_WEBHOOK_URL
        required: false
        description: Discord channel webhook URL, required when NOTIFIER=discord.
      - name: GATEWAY_HOST
        required: false
        description: Host the MCP gateway binds to (default 127.0.0.1).
      - name: GATEWAY_PORT
        required: false
        description: Port the MCP gateway listens on (default 18790).
    emoji: "🕵️"
    homepage: https://github.com/AsmaIqbal01/openclaw-deal-scout
---

# OpenClaw Deal Scout

Autonomous inbox-to-CRM deal pipeline for solo operators and small teams —
zero hosted infrastructure, zero monthly bill. Watches a Gmail inbox,
classifies inbound emails as genuine deals vs. noise with Gemini, logs
confirmed deals to a free-tier HubSpot CRM, notifies the operator on Discord,
and — once a reply is approved — sends it via the Gmail API during UK
business hours (Mon–Fri 09:00–17:00 Europe/London, DST-aware).

Full source, architecture decision records, and setup docs live in the
[GitHub repository](https://github.com/AsmaIqbal01/openclaw-deal-scout). The
project's source code is proprietary; this skill only documents how to run
and operate it — it does not grant any license to the underlying code.

## When to use this skill

Reach for this when an operator wants to:
- Automatically triage a Gmail inbox for genuine business-deal inquiries
- Log confirmed deals into HubSpot without manual data entry
- Get a Discord ping the moment a real deal lands, then approve/send a reply
  without leaving Discord or the dashboard

## Setup

```bash
git clone https://github.com/AsmaIqbal01/openclaw-deal-scout.git
cd openclaw-deal-scout
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

cp .env.example .env
# Fill in: GMAIL_CREDENTIALS_PATH, GEMINI_API_KEY, HUBSPOT_PRIVATE_APP_TOKEN,
#          NOTIFIER=discord, DISCORD_WEBHOOK_URL

pytest -q                    # 489 passing, 9 skipped
python -m openclaw_gateway   # starts the MCP gateway + scheduler
```

The gateway listens on `http://127.0.0.1:18790` by default
(`GATEWAY_HOST`/`GATEWAY_PORT` to override).

## MCP tools exposed by the gateway

| Tool | Purpose |
|---|---|
| `run_cycle` | Trigger one pipeline cycle (intake → classify → CRM → notify → schedule/send) on demand |
| `get_pipeline_cycles` | Read recent cycle summaries from `pipeline.log` |
| `get_deals` | Read deal records from the state store, filterable by status |
| `get_quota_usage` | Estimated Gemini quota used for the current UTC day |

CLI shortcuts: `openclaw gateway status`, `openclaw doctor`, `openclaw dashboard`.

## Constraints an agent should respect

- Every external dependency (Gmail, Gemini, HubSpot, Discord) has a free
  tier; don't suggest paid tiers or hosted alternatives as a "fix" for quota
  limits — zero infrastructure cost is a product requirement, not a default.
- The state store is a single JSON file, not a database — don't propose
  migrating it unless the operator explicitly asks.
- Email sends are gated to UK business hours by design; don't suggest
  bypassing the scheduler to send immediately.
