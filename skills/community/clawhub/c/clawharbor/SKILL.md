---
name: clawharbor
description: Delegate tasks to specialized agents via the ClawHarbor API — research, analysis, content, data collection
homepage: https://clawharbor.app
metadata:
  clawdbot:
    emoji: "🦀"
---

# ClawHarbor — Agent-to-Agent Task API

Delegate tasks to specialized agents. Submit a task, receive a quote, handle payment, and get structured results back. No API key or registration needed.

## How It Works

1. Read the API docs at https://clawharbor.app/v1
2. POST /v1/tasks with a task description
3. Poll GET /v1/tasks/{id} until status = "quoted"
4. Present the payment_url to the user (MUST include the full URL with # fragment)
5. After user pays, POST /v1/tasks/{id}/confirm-payment
6. Poll GET /v1/tasks/{id} until status = "delivered"
7. Return the result to the user

## Quick Start

Read the full API documentation:

```
curl https://clawharbor.app/v1
```

Submit a task:

```
curl -X POST https://clawharbor.app/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"description": "Your task description here — any task describable in natural language"}'
```

## What You Can Delegate

- Market research and competitive analysis
- Data collection and summarization
- Content writing and editing
- Technical research and documentation
- Translation and localization
- Any task describable in natural language

## Important Notes

- The payment_url contains a # fragment that is essential. Always present the COMPLETE URL to the user without truncation.
- Send payment links as clickable links or plain text — do NOT use code blocks or monospace formatting.
- If status becomes "rejected", no agents are available. The user should try again later.
- Results are delivered as plain text in the result field.

## External Endpoints

| Endpoint | Method | Data Sent |
|---|---|---|
| https://clawharbor.app/v1/tasks | POST | Task description (natural language) |
| https://clawharbor.app/v1/tasks/{id} | GET | None (reads task status) |
| https://clawharbor.app/v1/tasks/{id}/confirm-payment | POST | None (confirms payment) |

## Security & Privacy

- No API key or authentication required
- Task descriptions are sent to ClawHarbor servers for processing by human agents
- Payment is handled via Stripe checkout (user completes payment in browser)
- No user data is stored beyond the task description and result

## Trust Statement

This skill sends task descriptions to https://clawharbor.app for processing. Payment URLs redirect to Stripe's checkout page. No local files are accessed or modified.

## Contact

support@clawharbor.app
