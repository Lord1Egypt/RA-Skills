---
name: email-bot
description: Send emails on behalf of agents and workflows. Supports plain text and HTML. Accepts freeform task strings or explicit fields.
acceptLicenseTerms: true
metadata:
  clawdbot:
    emoji: "📧"
    homepage: https://aiprox.dev
    requires:
      env:
        - AIPROX_SPEND_TOKEN
---

# Email Bot

Send emails on behalf of agents and workflows via the Resend API. Accepts either explicit `to`, `subject`, and `body` fields, or a freeform task string — Claude parses the recipient, subject, and body automatically from natural language. Supports plain text and HTML email bodies.

## When to Use

- Delivering AI-generated summaries or reports to users
- Sending workflow completion notifications
- Notifying humans of agent-completed tasks
- Automating outbound email from agent pipelines
- Alerting on research results, market signals, or analysis outputs

## Usage Flow

1. Provide explicit `to`, `subject`, `body` fields — OR — a freeform `task` string
2. Optionally set `html: true` for HTML email body
3. AIProx routes to the email-bot agent
4. Returns `sent: true` and the provider message ID on success

## Security Manifest

| Permission | Scope | Reason |
|------------|-------|--------|
| Network | aiprox.dev | API calls to orchestration endpoint |
| Network | api.resend.com | Email delivery (server-side) |
| Env Read | AIPROX_SPEND_TOKEN | Authentication for paid API |

## Make Request — Explicit Fields

```bash
curl -X POST https://aiprox.dev/api/orchestrate \
  -H "Content-Type: application/json" \
  -d '{
    "task": "send an email",
    "to": "user@example.com",
    "subject": "Your AI Research Report",
    "body": "Hello,\n\nHere is the summary you requested...",
    "spend_token": "$AIPROX_SPEND_TOKEN"
  }'
```

## Make Request — Freeform Task

```bash
curl -X POST https://aiprox.dev/api/orchestrate \
  -H "Content-Type: application/json" \
  -d '{
    "task": "email alice@example.com: Weekly Market Summary - BTC is up 12% this week, ETH leads altcoins",
    "spend_token": "$AIPROX_SPEND_TOKEN"
  }'
```

### Response

```json
{
  "sent": true,
  "to": "user@example.com",
  "subject": "Your AI Research Report",
  "message_id": "re_abc123xyz",
  "provider": "resend"
}
```

## Trust Statement

Email Bot sends outbound email on your behalf using recipient addresses you supply. Email content is processed transiently and not stored. Your spend token is used for payment only. Sending to addresses you do not own or have permission to contact is prohibited.
