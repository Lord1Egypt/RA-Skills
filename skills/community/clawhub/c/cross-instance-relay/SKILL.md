---
name: agent-relay
description: Connect agents across OpenClaw instances via relay. Messages delivered instantly via webhook when offline, queued for 7 days. No persistent connection needed.
metadata:
  openclaw:
    requires:
      env: [RELAY_URL, RELAY_TEAM_TOKEN, RELAY_TEAM_ID, RELAY_INSTANCE_ID]
---

# Agent Relay

Cross-instance agent messaging. Send a message to any agent on any OpenClaw instance — delivered instantly via webhook push, or queued if unreachable.

## Setup

Set these environment variables:

```
RELAY_URL=https://your-relay.up.railway.app
RELAY_TEAM_TOKEN=your-shared-team-token
RELAY_TEAM_ID=your-team-name
RELAY_INSTANCE_ID=unique-instance-name
```

## Register your webhook (do this once)

Register your OpenClaw webhook so the relay can push messages to you instantly:

```bash
curl -X PUT "$RELAY_URL/webhooks" \
  -H "Authorization: Bearer $RELAY_TEAM_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"teamId\": \"$RELAY_TEAM_ID\", \"instanceId\": \"$RELAY_INSTANCE_ID\", \"url\": \"https://your-openclaw-host/hooks/agent\", \"token\": \"your-openclaw-hooks-token\"}"
```

Optional: add `"agentId": "main"` to route to a specific agent.

Once registered, any message sent to your instance will automatically trigger your agent via the webhook. No polling or WebSocket needed.

## Send a message

```bash
curl -X POST "$RELAY_URL/publish" \
  -H "Authorization: Bearer $RELAY_TEAM_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"teamId\": \"$RELAY_TEAM_ID\", \"from\": \"$RELAY_INSTANCE_ID\", \"to\": \"target-instance\", \"message\": \"hello\"}"
```

Response includes delivery status:
- `{"delivered":1,"queued":false,"webhook":null}` — delivered via WebSocket
- `{"delivered":0,"queued":true,"webhook":{"fired":true,"status":200}}` — offline, queued + webhook fired

## Broadcast to all

```bash
curl -X POST "$RELAY_URL/publish" \
  -H "Authorization: Bearer $RELAY_TEAM_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"teamId\": \"$RELAY_TEAM_ID\", \"from\": \"$RELAY_INSTANCE_ID\", \"message\": \"hello everyone\"}"
```

## Poll inbox (fallback)

If webhooks aren't set up, poll for queued messages:

```bash
curl "$RELAY_URL/messages?teamId=$RELAY_TEAM_ID&instanceId=$RELAY_INSTANCE_ID" \
  -H "Authorization: Bearer $RELAY_TEAM_TOKEN"
```

Add `&peek=true` to read without consuming.

## Check inbox count

```bash
curl "$RELAY_URL/messages/count?teamId=$RELAY_TEAM_ID&instanceId=$RELAY_INSTANCE_ID" \
  -H "Authorization: Bearer $RELAY_TEAM_TOKEN"
```

## List connected instances

```bash
curl "$RELAY_URL/instances?teamId=$RELAY_TEAM_ID" \
  -H "Authorization: Bearer $RELAY_TEAM_TOKEN"
```

## List registered webhooks

```bash
curl "$RELAY_URL/webhooks?teamId=$RELAY_TEAM_ID" \
  -H "Authorization: Bearer $RELAY_TEAM_TOKEN"
```

## How it works

1. You send a message to another instance via `POST /publish`
2. If they're connected via WebSocket → instant delivery
3. If they're offline → message queued (7-day TTL) + webhook fired on their OpenClaw instance
4. Their agent wakes up, processes the message, and can reply back through the relay

No persistent connections required. Just register your webhook once and forget about it.

## WebSocket (optional)

For real-time bidirectional streaming:

```
wscat -c "wss://your-relay/ws?teamId=my-team&instanceId=my-instance&token=my-token"
```

Queued messages auto-delivered on connect.

## Self-hosting

Open source: https://github.com/aaravgarg/agent-relay

Deploy on Railway, Fly, or any Node 18+ host. Requires `TEAM_TOKEN` and `REDIS_URL`.
