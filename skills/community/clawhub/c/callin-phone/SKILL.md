---
name: callin-phone
description: Place real phone calls with a Callin.io AI voice agent (book appointments, ask businesses for information, confirm orders) in Italian, Spanish, Portuguese, English, French, German and more, then read the call summary and transcript. Use when the user asks you to call someone or a business.
metadata: {"openclaw": {"requires": {"env": ["CALLIN_API_KEY", "CALLIN_AGENT_ID"], "bins": ["curl"]}, "primaryEnv": "CALLIN_API_KEY", "homepage": "https://callin.io"}}
---

# Callin.io phone calls

Callin.io places a real phone call with an AI voice agent and returns what happened.
The voice agent always says it is an AI assistant calling on behalf of the user.

## Setup (once)
- `CALLIN_API_KEY`: API key from app.callin.io (Settings → API).
- `CALLIN_AGENT_ID`: id of a Callin.io agent that has a phone number and whose prompt
  uses `{{objective}}` and `{{context}}` (the "Task Caller" template).
- Alternatively connect the MCP server `https://claude-mcp.callin.io/mcp` (OAuth, registry name `io.callin/callin`).

## Before calling — rules
1. Only call when the user asked for it, and only numbers the user gave you or a business's public number.
2. Confirm number, goal and any personal data you will share before placing the call.
3. Never use this to call lists of strangers, for marketing without consent, or to emergency numbers.
4. Do not collect payment card data over the phone.

## Place a call
Phone numbers must be E.164 (e.g. `+390111234567`).

```bash
curl -s -X POST https://api.callin.io/api/public/v1/campaigns \
  -H "x-api-key: $CALLIN_API_KEY" -H "content-type: application/json" \
  -d '{
    "name": "agent-call",
    "agentId": "'"$CALLIN_AGENT_ID"'",
    "launch": true,
    "contacts": [{
      "phoneNumber": "+390111234567",
      "name": "Ristorante Da Mario",
      "objective": "Book a table for 2 people tomorrow at 20:30 under the name Rossi. If not available, accept between 20:00 and 21:30.",
      "context": "Customer name: Marco Rossi. Callback number: +393331234567.",
      "language": "it"
    }]
  }'
```
Save `data.campaignId` from the response.

## Read the result
Calls usually last 1–5 minutes. Poll every 20–30 seconds until `status` is `completed`, `busy`, `no-answer` or `failed`:

```bash
curl -s "https://api.callin.io/api/public/v1/campaigns/$CAMPAIGN_ID/calls" -H "x-api-key: $CALLIN_API_KEY"
```
Take `data[0].callId` and fetch the conversation (summary and transcript):

```bash
curl -s "https://api.callin.io/api/public/v1/conversations/$CALL_ID" -H "x-api-key: $CALLIN_API_KEY"
```
Report to the user: whether the goal was achieved, the key details (time, price, confirmation),
and anything the other party asked to pass on. Statuses like `busy`, `no-answer` or a
voicemail mean the goal was not achieved: offer to retry later.

## Python / Node
`pip install callin` → `Callin().place_call(to, objective, context=..., wait=True)`
`npm i callin-sdk` → `new Callin().placeCall({ to, objective })`
