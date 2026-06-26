# fintech-support-agent

An OpenClaw skill that handles customer support for fintech and remittance
products. Resolves tier-1 tickets autonomously across any messaging channel
and hands off complex cases to humans with full context already written.

Built after reading 30,000 TapTap Send Trustpilot reviews. The same three
complaints showed up on loop. This skill handles all three.

---

## What it does

| Intent | What the agent does |
|---|---|
| Transfer status | Looks up the transaction via API, returns plain-language status |
| Refund request | Attempts recall if pending, logs dispute if delivered |
| Account issue | Checks suspension reason, routes KYC vs fraud vs other |
| KYC guidance | Returns the specific docs still needed for this customer |
| Complaint | Writes escalation summary, posts to webhook, gives case ref |
| Weekly digest | Sends ops team a markdown summary every Monday 08:00 |

---

## Setup

### 1. Install the skill

```bash
clawhub install fintech-support-agent
```

Or manually:

```bash
git clone https://github.com/nabeel/fintech-support-agent
cp -r fintech-support-agent ~/.openclaw/skills/
```

### 2. Set environment variables

Add these to your OpenClaw config (`~/.openclaw/openclaw.json`) under
`skills.entries`:

```json
{
  "skills": {
    "entries": {
      "fintech-support-agent": {
        "env": {
          "LLM_API_KEY": "your-openai-or-other-key",
          "TRANSFER_API_BASE_URL": "https://api.yourproduct.com/v1",
          "TRANSFER_API_KEY": "your-internal-api-key",
          "SUPPORT_EMAIL": "ops@yourproduct.com",
          "ESCALATION_WEBHOOK_URL": "https://hooks.slack.com/your-webhook"
        }
      }
    }
  }
}
```

### 3. Connect your channels

The skill works with whatever channels you have connected to OpenClaw:
WhatsApp, Telegram, web chat, email, Slack. No channel-specific config needed.

---

## How the API integration works

The skill expects your backend to expose these endpoints:

```
GET  /transfers/{ref}
GET  /customers/{customer_id}/transfers/latest
POST /transfers/{ref}/recall
POST /transfers/{ref}/dispute
GET  /customers/{customer_id}/status
GET  /customers/{customer_id}/kyc
```

If your API has different paths, update the `api_get` / `api_post` calls in
`handlers.py`. The handler logic stays the same.

If you don't have a live API yet, the skill degrades gracefully — the triage
still runs and the agent gives sensible responses based on what it knows.

---

## Testing without a live API

```bash
# Test the intent classifier
python3 triage.py "where is my money i sent yesterday"
# → TRANSFER_STATUS

python3 triage.py "my account is suspended and i don't know why"
# → ACCOUNT_ISSUE

# Test a handler (will return API_UNAVAILABLE gracefully)
python3 handlers.py transfer_status --customer-id test123 --ref TXN-456

# Generate a weekly digest from whatever's in the ticket log
python3 handlers.py weekly_digest
```

---

## Adapting for your product

The skill is intentionally generic. To tailor it:

- Update the escalation response times in `SKILL.md` (currently 4h normal, 1h high)
- Change the fraud-flagging keywords in `handlers.py` `handle_escalate()`
- Add product-specific intents to `triage.py` `keyword_fallback()`
- Add your own API endpoints to `handlers.py`

---

## Security notes

- API keys are injected via environment variables, never hardcoded
- The skill never asks customers for passwords, PINs, or card numbers
- Fraud-flagged accounts are never unblocked autonomously
- All ticket data is stored locally in `~/.openclaw/memory/support/`
- No data leaves your machine except via your own API and webhook

---

## License

MIT. Fork it, change it, ship it.
