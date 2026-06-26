# Setup Notes — Credential Reference

Quick reference for connecting credentials in the Lead Router workflow.

---

## Credential Nodes in the Workflow

### 1. Webhook Trigger (no credentials needed)
- n8n auto-generates the URL on activation
- Copy from: Webhook node → Parameters tab → Webhook URL

### 2. CRM / Log Destination (pick one)

**Google Sheets:**
- Credential type: `Google Sheets OAuth2 API`
- Needs: Google account with Sheets access
- Sheet must exist before first run; workflow writes to Sheet1 by default

**Airtable:**
- Credential type: `Airtable API`
- Needs: Airtable API key (Settings → Developer Hub → Personal access tokens)
- Base ID and Table name set in the Airtable node parameters

**HubSpot:**
- Credential type: `HubSpot API`
- Needs: Private App token (Settings → Integrations → Private Apps)
- Required scopes: `crm.objects.contacts.write`

### 3. Slack Alert (optional)
- Credential type: `Slack API`
- Needs: Bot token with `chat:write` scope
- Channel ID set in Slack node parameters (use channel ID, not name)

---

## Routing Score Thresholds (defaults)

| Score | Bucket | Action |
|-------|--------|--------|
| 7–10 | Hot | → CRM + Slack alert |
| 4–6 | Warm | → CRM, no alert |
| 1–3 | Cold | → Nurture list only |
| 0 | Spam/incomplete | → Discard |

Adjust in the `Lead Score + Route` Function node. Score logic is plain JS — easy to modify.

---

## Common Issues

**Webhook returns 404 after import:**
- Workflow must be **Activated** (toggle in top right) before the webhook goes live

**Duplicate leads appearing:**
- Check the `Dedup Check` node — ensure your CRM credential is connected and the lookup field matches your form's email field name

**Slack alerts not sending:**
- Verify the bot is invited to the target channel (`/invite @your-bot-name`)
- Check the channel ID (not channel name) is set correctly
