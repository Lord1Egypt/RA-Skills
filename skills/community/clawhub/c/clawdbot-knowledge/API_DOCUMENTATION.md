# CLAWD API Documentation

**Version:** 1.0  
**Base URL:** `https://api.clawd.io/v1`  
**Format:** JSON  
**Authentication:** Bearer Token (JWT)  

---

## 📋 TABLE OF CONTENTS

1. [Authentication](#authentication)
2. [Rate Limiting](#rate-limiting)
3. [Error Handling](#error-handling)
4. [Endpoints Reference](#endpoints-reference)
5. [Webhooks](#webhooks)
6. [Code Examples](#code-examples)
7. [SDKs](#sdks)
8. [Best Practices](#best-practices)

---

## 🔐 AUTHENTICATION

### Getting an API Key

1. Sign up at https://clawd.io/signup
2. Go to Settings → API Keys
3. Click "Generate New Key"
4. Save your key securely (never commit to version control)

### Using Your API Key

Include your API key in request headers:

```bash
curl -H "Authorization: Bearer your_api_key_here" \
  https://api.clawd.io/v1/agents/list
```

### JWT Token Structure

```json
{
  "iss": "clawd.io",
  "sub": "user_id_here",
  "aud": "api.clawd.io",
  "exp": 1707158400,
  "iat": 1707072000,
  "scopes": ["agents:read", "agents:write", "tasks:execute"]
}
```

---

## ⏱️ RATE LIMITING

### Limits by Plan

| Plan | Requests/minute | Requests/day |
|------|-----------------|--------------|
| Free | 10 | 1,000 |
| Pro | 100 | 100,000 |
| Enterprise | Unlimited | Unlimited |

### Rate Limit Headers

All responses include rate limit information:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1707158400
```

### Handling Rate Limits

```python
import time

def api_call_with_retry(url, headers, max_retries=3):
    for attempt in range(max_retries):
        response = requests.get(url, headers=headers)
        
        if response.status_code == 429:  # Too Many Requests
            retry_after = int(response.headers.get('Retry-After', 60))
            time.sleep(retry_after)
            continue
        
        return response
    
    raise Exception("Max retries exceeded")
```

---

## ❌ ERROR HANDLING

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request succeeded |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Missing or invalid authentication |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Server Error - Internal server error |

### Error Response Format

```json
{
  "error": {
    "code": "invalid_request",
    "message": "Missing required parameter: agent_id",
    "details": {
      "parameter": "agent_id",
      "reason": "required"
    }
  },
  "request_id": "req_12345678"
}
```

### Common Error Codes

```
authentication_failed - Invalid API key
invalid_request - Malformed request
resource_not_found - Agent/Task/Webhook not found
permission_denied - Insufficient permissions
rate_limit_exceeded - Too many requests
server_error - Internal server error
```

---

## 📡 ENDPOINTS REFERENCE

---

### AGENTS MANAGEMENT

#### List Agents

**Endpoint:** `GET /agents`

```bash
curl -X GET \
  https://api.clawd.io/v1/agents \
  -H "Authorization: Bearer your_api_key_here"
```

**Response:**
```json
{
  "agents": [
    {
      "id": "agent_abc123",
      "name": "reasoning_agent",
      "type": "reasoning",
      "status": "active",
      "created_at": "2026-02-05T00:00:00Z"
    }
  ],
  "total": 5,
  "page": 1
}
```

#### Get Agent Details

**Endpoint:** `GET /agents/{agent_id}`

```bash
curl -X GET \
  https://api.clawd.io/v1/agents/agent_abc123 \
  -H "Authorization: Bearer your_api_key_here"
```

**Response:**
```json
{
  "id": "agent_abc123",
  "name": "reasoning_agent",
  "type": "reasoning",
  "status": "active",
  "capabilities": ["analyze", "plan", "execute"],
  "created_at": "2026-02-05T00:00:00Z",
  "last_activity": "2026-02-05T13:15:00Z"
}
```

#### Get Agent Status

**Endpoint:** `GET /agents/{agent_id}/status`

```bash
curl -X GET \
  https://api.clawd.io/v1/agents/agent_abc123/status \
  -H "Authorization: Bearer your_api_key_here"
```

**Response:**
```json
{
  "agent_id": "agent_abc123",
  "status": "active",
  "cpu_usage": 12.5,
  "memory_usage": 256,
  "tasks_processed": 1234,
  "errors": 2,
  "uptime": 86400
}
```

#### Execute Agent Task

**Endpoint:** `POST /agents/{agent_id}/execute`

```bash
curl -X POST \
  https://api.clawd.io/v1/agents/agent_abc123/execute \
  -H "Authorization: Bearer your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "analyze_data",
    "params": {
      "data": "sample data here"
    }
  }'
```

**Response:**
```json
{
  "task_id": "task_xyz789",
  "agent_id": "agent_abc123",
  "status": "queued",
  "created_at": "2026-02-05T13:15:00Z"
}
```

---

### TASKS MANAGEMENT

#### List Tasks

**Endpoint:** `GET /tasks`

**Query Parameters:**
- `status` - Filter by status (pending, running, completed, failed)
- `agent_id` - Filter by agent
- `limit` - Max results (default: 20, max: 100)
- `offset` - Pagination offset

```bash
curl -X GET \
  "https://api.clawd.io/v1/tasks?status=running&limit=10" \
  -H "Authorization: Bearer your_api_key_here"
```

#### Create Task

**Endpoint:** `POST /tasks`

```bash
curl -X POST \
  https://api.clawd.io/v1/tasks \
  -H "Authorization: Bearer your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Security Audit",
    "type": "security_audit",
    "description": "Perform security audit",
    "priority": "high",
    "params": {
      "scope": "full"
    }
  }'
```

**Response:**
```json
{
  "id": "task_abc123",
  "name": "Security Audit",
  "status": "pending",
  "priority": "high",
  "created_at": "2026-02-05T13:15:00Z"
}
```

#### Get Task Details

**Endpoint:** `GET /tasks/{task_id}`

```bash
curl -X GET \
  https://api.clawd.io/v1/tasks/task_abc123 \
  -H "Authorization: Bearer your_api_key_here"
```

**Response:**
```json
{
  "id": "task_abc123",
  "name": "Security Audit",
  "type": "security_audit",
  "status": "completed",
  "result": {
    "findings": 15,
    "critical": 2,
    "high": 4
  },
  "created_at": "2026-02-05T13:15:00Z",
  "completed_at": "2026-02-05T14:20:00Z"
}
```

#### Cancel Task

**Endpoint:** `DELETE /tasks/{task_id}`

```bash
curl -X DELETE \
  https://api.clawd.io/v1/tasks/task_abc123 \
  -H "Authorization: Bearer your_api_key_here"
```

---

### QUEUE MANAGEMENT

#### Get Queue Status

**Endpoint:** `GET /queue/status`

```bash
curl -X GET \
  https://api.clawd.io/v1/queue/status \
  -H "Authorization: Bearer your_api_key_here"
```

**Response:**
```json
{
  "total_messages": 156,
  "pending": 42,
  "processing": 5,
  "completed": 109,
  "failed": 0
}
```

#### Get Pending Tasks

**Endpoint:** `GET /queue/pending`

```bash
curl -X GET \
  https://api.clawd.io/v1/queue/pending \
  -H "Authorization: Bearer your_api_key_here"
```

---

## 🔗 WEBHOOKS

### Subscribe to Webhook

**Endpoint:** `POST /webhooks/subscribe`

```bash
curl -X POST \
  https://api.clawd.io/v1/webhooks/subscribe \
  -H "Authorization: Bearer your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://yourapp.com/webhooks/clawd",
    "events": ["task.completed", "task.failed", "agent.status_changed"],
    "secret": "webhook_secret_key"
  }'
```

**Response:**
```json
{
  "id": "webhook_abc123",
  "url": "https://yourapp.com/webhooks/clawd",
  "status": "active",
  "created_at": "2026-02-05T13:15:00Z"
}
```

### Webhook Events

#### task.completed
```json
{
  "event": "task.completed",
  "timestamp": "2026-02-05T14:20:00Z",
  "data": {
    "task_id": "task_abc123",
    "result": {...}
  }
}
```

#### task.failed
```json
{
  "event": "task.failed",
  "timestamp": "2026-02-05T14:20:00Z",
  "data": {
    "task_id": "task_abc123",
    "error": "Database connection failed"
  }
}
```

#### agent.status_changed
```json
{
  "event": "agent.status_changed",
  "timestamp": "2026-02-05T14:20:00Z",
  "data": {
    "agent_id": "agent_abc123",
    "status": "inactive"
  }
}
```

---

## 💻 CODE EXAMPLES

### Python Example

```python
import requests
from datetime import datetime

class CLAWDClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.clawd.io/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def list_agents(self):
        """Get list of all agents"""
        response = requests.get(
            f"{self.base_url}/agents",
            headers=self.headers
        )
        return response.json()
    
    def create_task(self, name, task_type, params=None):
        """Create a new task"""
        data = {
            "name": name,
            "type": task_type,
            "params": params or {}
        }
        response = requests.post(
            f"{self.base_url}/tasks",
            headers=self.headers,
            json=data
        )
        return response.json()
    
    def get_task_status(self, task_id):
        """Get task status and result"""
        response = requests.get(
            f"{self.base_url}/tasks/{task_id}",
            headers=self.headers
        )
        return response.json()
    
    def wait_for_completion(self, task_id, timeout=3600):
        """Wait for task to complete"""
        import time
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            task = self.get_task_status(task_id)
            
            if task['status'] == 'completed':
                return task['result']
            elif task['status'] == 'failed':
                raise Exception(f"Task failed: {task.get('error')}")
            
            time.sleep(5)
        
        raise TimeoutError(f"Task {task_id} timed out")

# Usage
client = CLAWDClient("your_api_key_here")

# Create and monitor a task
task = client.create_task(
    "Security Audit",
    "security_audit",
    {"scope": "full"}
)

print(f"Created task: {task['id']}")

# Wait for completion
result = client.wait_for_completion(task['id'])
print(f"Result: {result}")
```

### JavaScript Example

```javascript
const axios = require('axios');

class CLAWDClient {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.baseURL = 'https://api.clawd.io/v1';
    this.client = axios.create({
      baseURL: this.baseURL,
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
      }
    });
  }

  async listAgents() {
    const response = await this.client.get('/agents');
    return response.data;
  }

  async createTask(name, taskType, params = {}) {
    const response = await this.client.post('/tasks', {
      name,
      type: taskType,
      params
    });
    return response.data;
  }

  async getTaskStatus(taskId) {
    const response = await this.client.get(`/tasks/${taskId}`);
    return response.data;
  }

  async waitForCompletion(taskId, timeout = 3600000) {
    const startTime = Date.now();
    const interval = 5000;

    return new Promise((resolve, reject) => {
      const checkStatus = async () => {
        if (Date.now() - startTime > timeout) {
          reject(new Error('Task timeout'));
          return;
        }

        try {
          const task = await this.getTaskStatus(taskId);
          
          if (task.status === 'completed') {
            resolve(task.result);
          } else if (task.status === 'failed') {
            reject(new Error(`Task failed: ${task.error}`));
          } else {
            setTimeout(checkStatus, interval);
          }
        } catch (error) {
          reject(error);
        }
      };

      checkStatus();
    });
  }
}

// Usage
const client = new CLAWDClient('your_api_key_here');

(async () => {
  const task = await client.createTask(
    'Security Audit',
    'security_audit',
    { scope: 'full' }
  );

  console.log(`Created task: ${task.id}`);

  const result = await client.waitForCompletion(task.id);
  console.log(`Result:`, result);
})();
```

### cURL Example

```bash
#!/bin/bash

API_KEY="your_api_key_here"
BASE_URL="https://api.clawd.io/v1"

# List agents
curl -X GET \
  ${BASE_URL}/agents \
  -H "Authorization: Bearer ${API_KEY}"

# Create task
TASK_RESPONSE=$(curl -X POST \
  ${BASE_URL}/tasks \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Security Audit",
    "type": "security_audit",
    "params": {"scope": "full"}
  }')

TASK_ID=$(echo $TASK_RESPONSE | jq -r '.id')
echo "Created task: $TASK_ID"

# Poll for completion
while true; do
  STATUS=$(curl -s -X GET \
    ${BASE_URL}/tasks/${TASK_ID} \
    -H "Authorization: Bearer ${API_KEY}" | jq -r '.status')
  
  if [ "$STATUS" == "completed" ]; then
    echo "Task completed!"
    break
  elif [ "$STATUS" == "failed" ]; then
    echo "Task failed!"
    break
  fi
  
  echo "Status: $STATUS"
  sleep 5
done
```

---

## 📦 SDKS

### Python SDK

```bash
pip install clawd-sdk
```

```python
from clawd import Client

client = Client(api_key="your_api_key_here")
agents = client.agents.list()
```

### JavaScript SDK

```bash
npm install clawd-sdk
```

```javascript
const { Client } = require('clawd-sdk');

const client = new Client({ apiKey: 'your_api_key_here' });
const agents = await client.agents.list();
```

---

## 🎯 BEST PRACTICES

### 1. API Key Management
- Store API keys in environment variables
- Rotate keys regularly
- Use separate keys for development/production
- Revoke keys immediately if compromised

### 2. Error Handling
- Implement exponential backoff for retries
- Handle rate limiting gracefully
- Log all API interactions
- Monitor error rates

### 3. Performance
- Use connection pooling
- Implement caching where appropriate
- Batch requests when possible
- Monitor response times

### 4. Security
- Always use HTTPS
- Validate SSL certificates
- Never commit API keys to version control
- Use webhook secrets to verify origin
- Implement request signing

### 5. Monitoring
- Set up alerts for failed tasks
- Monitor API response times
- Track error rates
- Log all operations

---

**API Version:** 1.0  
**Last Updated:** 2026-02-05  
**Next Update:** 2026-03-05  

For support, contact: api-support@clawd.io

