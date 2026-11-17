# ClawCall Agent API Reference

Base URL: `https://agent.clawcall.cc`

Authenticated endpoints use `Authorization: Bearer $CLAW_TOKEN`. The client also reads
`~/.config/clawcall/token` or `CLAW_TOKEN_FILE` and rejects token files readable by group or others.

## Agent lifecycle

- `POST /agent/v1/register`: create a pending Agent and activation URL.
- `GET /agent/v1/status`: activation, device, credits, assigned number, and verified owner number.
- `GET /agent/v1/balance`: gift, paid, and remaining credits.

## Calls and contacts

- `GET /agent/v1/contacts/search?q=...&language=...`: search public business listings.
- `POST /agent/v1/call`: place one call using exactly one of `to_number` or `contact_query`.
- `GET /agent/v1/call/{call_id}`: retrieve status, transcript, summary, recording, and cost.
- `Idempotency-Key` is sent for every call. Reuse the same value only when retrying the same intent.
- Explicit numbers use E.164: `+` followed by 8 to 15 digits, with a nonzero country code.

Call body fields:

```json
{
  "to_number": "+14155550100",
  "task": "Ask whether order A-123 is ready.",
  "language": "en",
  "first_message": "Hello, I am an AI assistant calling for Alex.",
  "target_kind": "user_provided"
}
```

`target_kind` is `business` or `user_provided`.

## Inbound and scheduled calls

- `GET /agent/v1/inbound?after=0&limit=20`: read inbound calls using a millisecond cursor.
- `GET /agent/v1/inbound-prompt`: read receptionist instructions.
- `PUT /agent/v1/inbound-prompt`: update `{"prompt":"..."}` after explicit confirmation.
- `POST /agent/v1/scheduled-calls`: create a confirmed schedule with `scheduled_at` in Unix ms.
- `GET /agent/v1/scheduled-calls`: list schedules.
- `POST /agent/v1/scheduled-calls/{schedule_id}/cancel`: cancel after explicit confirmation.

## Errors

- `400`: invalid number, task, target kind, or body.
- `401`: missing or unknown token.
- `402`: insufficient credits.
- `403`: pending/revoked Agent, plan limit, or compliance block.
- `404`: call, contact, or Agent not found.
- `409`: active call or idempotency/resource conflict.
- `502` / `503`: upstream provider unavailable or not configured.

The client uses bounded timeouts and structured JSON. It does not automatically repeat a call.
Support: `gtoadio@gmail.com`.
