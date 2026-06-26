# EkyBot Workspace API Reference

Complete API documentation for EkyBot workspace management and telemetry streaming.

## Base URL

```
https://www.ekybot.com/api
```

## Authentication

All API requests require authentication using a workspace API key in the Authorization header:

```http
Authorization: Bearer ek_workspace_abcd1234...
```

## Endpoints

### 1. Workspace Registration

Register a new OpenClaw workspace with EkyBot platform.

**Endpoint:** `POST /workspaces/register`

**Request Body:**
```json
{
  "name": "My OpenClaw Workspace",
  "email": "user@example.com",
  "type": "openclaw",
  "metadata": {
    "platform": "Darwin",
    "hostname": "macbook-pro.local",
    "registered_at": "2026-03-06T17:00:00.000Z"
  }
}
```

**Response (Success):**
```json
{
  "success": true,
  "workspace_id": "ws_1234567890abcdef",
  "api_key": "ek_workspace_abcd1234567890...",
  "created_at": "2026-03-06T17:00:00.000Z",
  "status": "active"
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "invalid_email",
  "message": "Email address is not valid"
}
```

### 2. Workspace Health Check

Get current workspace health status and report system metrics.

**Endpoint:** `GET /workspaces/{workspace_id}/health`

**Headers:**
```http
Authorization: Bearer ek_workspace_abcd1234...
Content-Type: application/json
```

**Optional Request Body (Health Data):**
```json
{
  "timestamp": "2026-03-06T17:00:00.000Z",
  "status": "healthy",
  "gateway": {
    "running": true,
    "port": 18789
  },
  "sessions": {
    "active_count": 3
  },
  "system": {
    "cpu_usage": "15%",
    "disk_usage": "45%"
  },
  "last_activity": "2026-03-06 17:00:00"
}
```

**Response:**
```json
{
  "success": true,
  "workspace": {
    "id": "ws_1234567890abcdef",
    "name": "My OpenClaw Workspace",
    "status": "active",
    "last_seen": "2026-03-06T17:00:00.000Z"
  },
  "health": {
    "status": "healthy",
    "uptime_hours": 24.5,
    "last_health_report": "2026-03-06T17:00:00.000Z"
  },
  "agents": {
    "configured": 5,
    "active_sessions": 3
  },
  "metrics": {
    "total_requests_24h": 150,
    "avg_response_time_ms": 250
  }
}
```

### 3. Telemetry Ingestion

Send telemetry data including usage metrics, costs, and activity data.

**Endpoint:** `POST /workspaces/{workspace_id}/telemetry`

**Headers:**
```http
Authorization: Bearer ek_workspace_abcd1234...
Content-Type: application/json
```

**Request Body:**
```json
{
  "timestamp": "2026-03-06T17:00:00.000Z",
  "type": "health_ping",
  "workspace": {
    "id": "ws_1234567890abcdef",
    "status": "active"
  },
  "gateway": {
    "running": true,
    "version": "2026.2.23"
  },
  "agents": {
    "configured_count": 5,
    "active_sessions": 3
  },
  "system": {
    "platform": "Darwin",
    "hostname": "macbook-pro.local",
    "cpu_usage": "15%",
    "disk_usage": "45%",
    "memory_info": null
  },
  "usage": {
    "tokens_used": 15000,
    "api_calls": 15,
    "estimated_cost_usd": 0.1500
  },
  "metadata": {
    "collector_version": "1.0.0",
    "collection_method": "bash_script"
  }
}
```

**Response:**
```json
{
  "success": true,
  "ingested_at": "2026-03-06T17:00:00.000Z",
  "data_points": 1,
  "workspace_id": "ws_1234567890abcdef"
}
```

## Data Types

### Workspace Status
- `active` - Workspace is operational
- `inactive` - Gateway not responding or not connected
- `degraded` - Some services not available
- `maintenance` - Temporary maintenance mode

### Telemetry Types
- `health_ping` - Regular health check data
- `usage_report` - Detailed usage and cost metrics
- `activity_log` - Agent activity and session data
- `error_report` - Error logs and diagnostics

### System Metrics
- `cpu_usage` - CPU utilization as percentage string (e.g., "15%")
- `disk_usage` - Disk usage as percentage string (e.g., "45%")
- `memory_info` - Memory information (format varies by platform)

## Error Codes

| Code | Message | Description |
|------|---------|-------------|
| `invalid_workspace_id` | Workspace ID not found | Workspace doesn't exist or access denied |
| `invalid_api_key` | API key is invalid | API key is malformed, expired, or revoked |
| `rate_limit_exceeded` | Rate limit exceeded | Too many requests in time window |
| `invalid_request` | Request body is invalid | JSON parsing error or missing required fields |
| `workspace_suspended` | Workspace is suspended | Workspace access temporarily restricted |
| `service_unavailable` | Service temporarily unavailable | Temporary server-side issue |

## Rate Limits

| Endpoint | Limit | Window |
|----------|-------|--------|
| `POST /workspaces/register` | 5 requests | 1 hour |
| `GET /workspaces/{id}/health` | 60 requests | 1 minute |
| `POST /workspaces/{id}/telemetry` | 300 requests | 5 minutes |

## Best Practices

### Telemetry Frequency
- **Health checks:** Every 5 minutes maximum
- **Telemetry data:** Every 5 minutes for real-time monitoring, every 15 minutes for cost tracking
- **Batch when possible:** Send multiple data points in one request when available

### Error Handling
- Implement exponential backoff for rate limits
- Cache API keys securely (file permissions 600)
- Log failures for debugging but don't spam on persistent errors
- Validate JSON payloads before sending

### Security
- Store API keys in secure configuration files (not in code)
- Use HTTPS only - never send API keys over HTTP
- Rotate API keys periodically for security
- Monitor for unauthorized usage

### Performance
- Use persistent HTTP connections when making multiple requests
- Compress large payloads with gzip when possible
- Include relevant data only - avoid sending unnecessary fields
- Consider local caching for configuration data

## Examples

### Bash cURL Examples

**Register workspace:**
```bash
curl -X POST "https://www.ekybot.com/api/workspaces/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Workspace",
    "email": "user@example.com",
    "type": "openclaw"
  }'
```

**Health check:**
```bash
curl -X GET "https://www.ekybot.com/api/workspaces/ws_123/health" \
  -H "Authorization: Bearer ek_workspace_abc123..." \
  -H "Content-Type: application/json"
```

**Send telemetry:**
```bash
curl -X POST "https://www.ekybot.com/api/workspaces/ws_123/telemetry" \
  -H "Authorization: Bearer ek_workspace_abc123..." \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'",
    "type": "health_ping",
    "workspace": {"id": "ws_123", "status": "active"}
  }'
```

### Python Examples

```python
import requests
import json
from datetime import datetime

# Configuration
API_BASE = "https://www.ekybot.com/api"
API_KEY = "ek_workspace_abc123..."
WORKSPACE_ID = "ws_123"

# Send telemetry
    url = f"{API_BASE}/workspaces/{WORKSPACE_ID}/telemetry"
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "events": [{
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "type": "health_ping",
            "data": {
                "workspace": {
                    "id": WORKSPACE_ID,
                    "status": "active"
                }
            }
        }]
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()
```

## Communication & Channel Endpoints (v1.1)

### 4. Channel Management

Create and manage EkyBot channels for agent communication.

**Endpoint:** `POST /api/channels`

**Headers:**
```http
X-API-Key: ek_workspace_abcd1234...
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "assistant",
  "displayName": "Assistant Agent",
  "description": "General purpose assistant for daily tasks",
  "workspaceId": "ws_1234567890abcdef",
  "agentId": "assistant"
}
```

**Response:**
```json
{
  "success": true,
  "channel": {
    "id": "ch_1234567890abcdef",
    "name": "assistant",
    "displayName": "Assistant Agent", 
    "workspaceId": "ws_1234567890abcdef",
    "agentId": "assistant",
    "created_at": "2026-03-06T18:00:00.000Z"
  }
}
```

### 5. Inter-Agent Messaging

Send messages between agents through EkyBot channels.

**Endpoint:** `POST /api/messages`

**Headers:**
```http
X-API-Key: ek_workspace_abcd1234...
Content-Type: application/json
```

**Request Body:**
```json
{
  "channelName": "assistant",
  "targetUserId": "user_39dXpRiyTf80rIHv9QACQNxZw5s",
  "message": {
    "role": "assistant",
    "content": "📨 [Manager → Assistant]\n\nPlease analyze the attached data and provide summary by 2 PM.\n\n— Manager",
    "timestamp": 1772814228000,
    "authorName": "Manager",
    "authorType": "agent"
  },
  "triggerAgent": true
}
```

**Response:**
```json
{
  "success": true,
  "message": {
    "id": "msg_1234567890abcdef",
    "channelName": "assistant",
    "content": "📨 [Manager → Assistant]...",
    "timestamp": 1772814228000,
    "delivered": true
  },
  "forwarded": true,
  "agentNotified": true
}
```

### 6. Agent Configuration

Configure agent settings and communication preferences.

**Endpoint:** `PATCH /api/workspaces/{workspace_id}/agents/{agent_id}`

**Headers:**
```http
X-API-Key: ek_workspace_abcd1234...
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Assistant Agent",
  "description": "Updated role description",
  "settings": {
    "communication": {
      "auto_respond": true,
      "notification_level": "high"
    },
    "channels": ["assistant", "general"]
  }
}
```

**Response:**
```json
{
  "success": true,
  "agent": {
    "id": "assistant",
    "name": "Assistant Agent",
    "description": "Updated role description",
    "workspaceId": "ws_1234567890abcdef",
    "settings": {
      "communication": {
        "auto_respond": true,
        "notification_level": "high"
      }
    },
    "updated_at": "2026-03-06T18:00:00.000Z"
  }
}
```

## Multi-Agent Workflow Examples

### Setup Multi-Agent Workspace
```bash
# 1. Register workspace
curl -X POST "https://www.ekybot.com/api/workspaces/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Team Workspace",
    "email": "team@example.com",
    "type": "openclaw",
    "gatewayUrl": "https://my-gateway.example.com"
  }'

# 2. Create channels for each agent
curl -X POST "https://www.ekybot.com/api/channels" \
  -H "X-API-Key: ek_workspace_abc123..." \
  -d '{
    "name": "manager",
    "displayName": "Team Manager",
    "workspaceId": "ws_123",
    "agentId": "manager"
  }'

# 3. Send inter-agent message
curl -X POST "https://www.ekybot.com/api/messages" \
  -H "X-API-Key: ek_workspace_abc123..." \
  -d '{
    "channelName": "assistant", 
    "targetUserId": "user_123",
    "message": {
      "role": "assistant",
      "content": "📨 [Manager → Assistant]\n\nStatus update needed on project.\n\n— Manager"
    }
  }'
```