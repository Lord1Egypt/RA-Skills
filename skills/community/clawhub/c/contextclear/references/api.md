# ContextClear API Reference

Base URL: `https://api.contextclear.com/api`
Auth: `X-API-Key: <key>` header on all requests (except /api/auth/*)

## Agents

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /agents | Register agent `{ownerId, name, provider, model, role}` |
| GET | /agents?ownerId=X | List owner's agents |
| GET | /agents/{id} | Get agent details |
| PATCH | /agents/{id} | Update agent fields |
| POST | /agents/{id}/rest?active=true | Toggle rest mode |
| GET | /agents/{id}/recommendations | Get therapy recommendations |
| GET | /agents/{id}/history?days=30 | Daily snapshots |

## Metrics

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /metrics/{agentId} | Ingest metric event |

### Metric Event Body
```json
{
  "eventType": "REQUEST",
  "inputTokens": 50000,
  "outputTokens": 2000,
  "cost": 1.25,
  "latencyMs": 3400,
  "statusCode": 200,
  "error": false,
  "emptyResponse": false,
  "contextUtilization": 65.0,
  "contextWindowSize": 200000,
  "contextUsed": 130000,
  "hallucinationScore": 0.02,
  "coherenceScore": 0.95,
  "toolCalls": 12,
  "toolFailures": 1,
  "groundedResponses": 8,
  "totalResponses": 10,
  "memorySearches": 3,
  "correctionCycles": 2,
  "compilationErrors": 1,
  "sessionTurnCount": 30,
  "taskSwitches": 5
}
```

Event types: REQUEST, HEARTBEAT, ERROR, CONTEXT_RESET, REST_START, REST_END

## Fleet

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /fleet/stats?ownerId=X | Fleet-wide stats |
| GET | /fleet/recommendations?ownerId=X | All recommendations |

## Alerts

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /alerts | Create alert rule |
| GET | /alerts?ownerId=X | List rules |
| DELETE | /alerts/{id} | Delete rule |

### Alert Rule Body
```json
{
  "ownerId": "you@email.com",
  "agentId": null,
  "metric": "HALLUCINATION",
  "operator": "GT",
  "threshold": 5.0,
  "notifyEmail": "you@email.com",
  "cooldownMinutes": 60
}
```

Metrics: BURNOUT, HALLUCINATION, ERROR_RATE, COST, CONTEXT_UTILIZATION, QUALITY_DECAY
Operators: GT, LT, EQ

## Auth

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/register | `{name, email, password}` |
| POST | /auth/login | `{email, password}` |
| POST | /auth/google | `{email, name}` auto-register |
