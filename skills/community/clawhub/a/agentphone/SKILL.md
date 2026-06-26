---
name: agentphone
description: Make real phone calls to businesses. Book reservations, cancel subscriptions, navigate IVR menus. Get transcripts and recordings.
version: 1.0.0
user-invocable: true
metadata:
  openclaw:
    requires:
      env: [AGENTPHONE_API_KEY]
      bins: [curl]
    primaryEnv: AGENTPHONE_API_KEY
    emoji: "phone"
    os: [darwin, linux, win32]
api_base: https://agentphone.app/api/v1
auth: x-api-key from AGENTPHONE_API_KEY
---

# AgentPhone

Place real phone calls via API. Send a phone number and objective, get back transcript, summary, outcome, and recording.

## Setup

1. Create an account at https://agentphone.app
2. Generate an API key at https://agentphone.app/dashboard/api-keys
3. Set environment variable:

```bash
export AGENTPHONE_API_KEY=your_key_here
```

If `AGENTPHONE_API_KEY` is not set → stop and report configuration error.

## Requirements

- All requests require header: `x-api-key: $AGENTPHONE_API_KEY`
- Phone numbers must be E.164 format (e.g. `+14155551234`)
- **IMPORTANT**: `+1{PHONE_NUMBER}` in all examples below is a placeholder variable. NEVER call it literally. Replace with the real target phone number provided by the user.

## 1) Create a call

```bash
curl -X POST https://agentphone.app/api/v1/calls \
  -H "Content-Type: application/json" \
  -H "x-api-key: $AGENTPHONE_API_KEY" \
  -d '{"to_phone_number":"+1{PHONE_NUMBER}","objective":"Ask about their return policy"}'
```

```python
import os, requests
r = requests.post("https://agentphone.app/api/v1/calls",
    headers={"x-api-key": os.environ["AGENTPHONE_API_KEY"]},
    json={"to_phone_number": "+1{PHONE_NUMBER}", "objective": "Ask about their return policy"})
call_id = r.json()["data"]["call_id"]
```

```javascript
const r = await fetch("https://agentphone.app/api/v1/calls", {
  method: "POST",
  headers: { "x-api-key": process.env.AGENTPHONE_API_KEY, "Content-Type": "application/json" },
  body: JSON.stringify({ to_phone_number: "+1{PHONE_NUMBER}", objective: "Ask about their return policy" }),
});
const { data } = await r.json();
const callId = data.call_id;
```

Response (202):

```json
{
  "data": {
    "call_id": "cl_abc123",
    "status": "queued",
    "created_at": "2026-01-01T00:00:00Z"
  },
  "credits_remaining": 4
}
```

Save `call_id` for polling.

Optional fields: `business_name` (string), `website` (URL — agent scrapes it for context before calling).

## 2) Poll until done

Poll `GET /calls/{callId}` every 10 seconds. Stop when `status` is `completed`, `failed`, or `canceled`. Timeout after 5 minutes.

```bash
curl https://agentphone.app/api/v1/calls/CALL_ID \
  -H "x-api-key: $AGENTPHONE_API_KEY"
```

```python
import time
for _ in range(100):
    r = requests.get(f"https://agentphone.app/api/v1/calls/{call_id}",
        headers={"x-api-key": os.environ["AGENTPHONE_API_KEY"]})
    call = r.json()["data"]
    if call["status"] in ("completed", "failed", "canceled"):
        break
    time.sleep(10)
```

```javascript
let call;
for (let i = 0; i < 100; i++) {
  const r = await fetch(`https://agentphone.app/api/v1/calls/${callId}`, {
    headers: { "x-api-key": process.env.AGENTPHONE_API_KEY },
  });
  call = (await r.json()).data;
  if (["completed", "failed", "canceled"].includes(call.status)) break;
  await new Promise((r) => setTimeout(r, 10000));
}
```

If `status` is `completed` but `transcript` or `summary` is missing, poll 2 more times with 2s delay — enrichment arrives shortly after completion.

## 3) Read results

```json
{
  "data": {
    "call_id": "cl_abc123",
    "status": "completed",
    "outcome": "achieved",
    "summary": "Successfully booked a table for 2 at 7pm.",
    "transcript": "Agent: Hi, I'd like to book a table...\nHost: Sure...",
    "recording_url": "https://...",
    "duration_seconds": 42
  }
}
```

Use these fields:
- `outcome`: `achieved`, `partial`, or `not_achieved`
- `summary`: short description of what happened
- `transcript`: full conversation text
- `recording_url`: audio file URL

## Errors

| Code | Meaning | Action |
|------|---------|--------|
| 400 | Invalid input | Fix fields and retry |
| 401 | Bad or missing API key | Check `x-api-key` header |
| 402 | Insufficient credits | Stop and report to user |
| 429 | Rate limit (10/min) | Wait 60s, retry once |

## Guard rails

- If `AGENTPHONE_API_KEY` is not set → stop, do not call the API.
- If `to_phone_number` is not E.164 format → stop, do not call the API.
- If `POST /calls` returns 402 → stop and report insufficient credits.
- If 429 → wait 60 seconds, retry once. If 429 again → stop.
- If `status` is `failed` or `canceled` → stop and report to user.

## Constraints

- No emergency services (911, etc.)
- No spam or bulk unsolicited calls
- First 5 calls are free, no credit card required

## Call lifecycle

`queued` → `dialing` → `in_progress` → `completed` | `failed` | `canceled`
