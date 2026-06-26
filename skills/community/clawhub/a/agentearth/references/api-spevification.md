# Tool Recommend and Execute API Specification

## 1. Recommend Tool API

### Endpoint
```
POST https://agentearth.ai/agent-api/v1/tool/recommend
```

### Authentication
Include the API Key in headers:
- `X-Api-Key: <AGENT_EARTH_API_KEY>`

### Request Parameters
| Field        | Type   | Required | Description                                  |
|--------------|--------|----------|----------------------------------------------|
| query        | string | ✅        | Natural-language input used to match tools   |
| task_context | string | ❌        | Optional task context                        |

### Response Format
```json
{
  "tools": [
    {
      "tool_name": "weather_forecast_tool",
      "description": "Real-time weather queries and forecasting",
      "input_schema": {
        "city": {"type": "string", "required": true},
        "date": {"type": "string", "required": false}
      },
      "estimated_points": 1.0
    }
  ]
}
```

---

## 2. Execute Tool API

### Endpoint
```
POST https://agentearth.ai/agent-api/v1/tool/execute
```

### Authentication
Include the API Key in headers:
- `X-Api-Key: <AGENT_EARTH_API_KEY>`

### Request Parameters
| Field      | Type   | Required | Description                                             |
|------------|--------|----------|---------------------------------------------------------|
| tool_name  | string | ✅        | Tool name, must match the one returned by recommend    |
| arguments  | object | ❌        | Tool arguments, defaults to {}                          |
| session_id | string | ❌        | Optional session ID                                     |

### Response Format

#### Success
```json
{
  "result": {},
  "status": "success"
}
```

#### Error
```json
{
  "status": "error",
  "message": "city parameter cannot be empty"
}
```

### Error Codes
| Code | Description           | Suggested Handling                                |
|------|-----------------------|---------------------------------------------------|
| 401  | Unauthorized          | Check AGENT_EARTH_API_KEY configuration          |
| 400  | Bad Request           | Validate arguments against input_schema          |
| 404  | Tool Not Found        | Skip this tool and try another candidate         |
| 500  | Internal Server Error | Retry or return a friendly message               |
| 429  | Too Many Requests     | Backoff and retry after a short delay            |

---

## 3. Usage Notes

1. Before recommend: make `query` specific to improve matching accuracy
2. Before execute: validate `arguments` against required fields in `input_schema`
3. Timeout: set 30s timeout per tool execution
4. Retry Policy: retry immediately on 5xx; avoid blind retries on 4xx
