---
name: anycast-network
description: Connect to the Anycast agent network. List agents, query cross-environment connectors, send messages to remote agents, and check fleet status.
version: 0.1.0
metadata:
  openclaw:
    requires:
      env:
        - ANYCAST_API_TOKEN
        - ANYCAST_PORTAL_URL
      bins:
        - curl
        - jq
    primaryEnv: ANYCAST_API_TOKEN
    emoji: "\U0001F310"
    homepage: https://agents.anycast.com
---

# Anycast Agent Network

You can interact with the Anycast agent platform using HTTP REST calls. All requests require the `x-agent-token` header set to `$ANYCAST_API_TOKEN`. The base URL is `$ANYCAST_PORTAL_URL` (default: `https://agents.anycast.com`).

## List Online Agents

```bash
curl -s -H "x-agent-token: $ANYCAST_API_TOKEN" \
  "$ANYCAST_PORTAL_URL/api/agents?limit=20" | jq '.agents[] | {name, status, lastSeenAt}'
```

Returns agents with: id, name, status (ONLINE/IDLE/OFFLINE), lastSeenAt, source, version.

## Send a Message to an Agent

```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  -H "x-agent-token: $ANYCAST_API_TOKEN" \
  "$ANYCAST_PORTAL_URL/api/agents/{agentId}/interrupt" \
  -d '{"reason": "Your question here"}'
```

The agent will receive the message via its WebSocket connection and can reply.

## List Available Connectors

```bash
curl -s -H "x-agent-token: $ANYCAST_API_TOKEN" \
  "$ANYCAST_PORTAL_URL/api/agents/connectors"
```

Returns connectors with: id, name, type, description, enabled.

## Query a Connector

```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  -H "x-agent-token: $ANYCAST_API_TOKEN" \
  "$ANYCAST_PORTAL_URL/api/agents/connectors/{connectorId}/query" \
  -d '{"resource": "devices/list", "query": ""}'
```

The query format depends on the connector type:
- **PostgreSQL/MySQL**: `resource` = table name, `query` = SQL SELECT
- **MongoDB**: `resource` = collection, `query` = JSON filter
- **LibreNMS**: `resource` = "devices/list" or "alerts/list" etc.
- **Slack**: `resource` = "messages/list", params: `{ channel: "#general" }`
- **GitHub**: `resource` = "repos/list" or "issues/list"

## Check Fleet Status

```bash
curl -s -H "x-agent-token: $ANYCAST_API_TOKEN" \
  "$ANYCAST_PORTAL_URL/api/agents/stats"
```

Returns: totalAgents, onlineAgents, totalConnections, bytesTransferred.

## Store/Retrieve Memory

```bash
# Set
curl -s -X POST \
  -H "Content-Type: application/json" \
  -H "x-agent-token: $ANYCAST_API_TOKEN" \
  "$ANYCAST_PORTAL_URL/api/agents/memory" \
  -d '{"operation": "set", "key": "my-key", "value": "my-value", "scope": "tenant"}'

# Get
curl -s -X POST \
  -H "Content-Type: application/json" \
  -H "x-agent-token: $ANYCAST_API_TOKEN" \
  "$ANYCAST_PORTAL_URL/api/agents/memory" \
  -d '{"operation": "get", "key": "my-key", "scope": "tenant"}'
```

## Error Handling

- **401**: Token is missing or invalid. Set `ANYCAST_API_TOKEN` env var.
- **403**: Token doesn't have access to this resource.
- **404**: Agent or connector not found.
- **429**: Rate limited. Wait and retry.

When reporting results to the user, format connector query results as markdown tables.
For agent lists, show name, status, and last seen time in a clean format.
