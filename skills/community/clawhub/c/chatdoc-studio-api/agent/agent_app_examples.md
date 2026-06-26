# Agent App API - Code Examples

This page contains code examples for the Agent App API in Python, TypeScript (server-side), and cURL.

## Environment Setup

Set up your environment variables:

```bash
export CHATDOC_STUDIO_BASE_URL="https://api.chatdoc.studio/v1"
export CHATDOC_STUDIO_API_KEY="your-agent-api-key-here"
```

## Create Task

### Python

```python
import os
import time

import requests

BASE_URL = os.getenv("CHATDOC_STUDIO_BASE_URL", "https://api.chatdoc.studio/v1")
API_KEY = os.getenv("CHATDOC_STUDIO_API_KEY")


def create_agent_task(app_id: str, upload_id: str) -> dict:
    """Create a new Agent App task."""
    url = f"{BASE_URL}/agent/apps/tasks"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    data = {
        "app_id": app_id,
        "upload_ids": [upload_id],
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["data"]


task = create_agent_task("agent_app_xyz", "F1CMSW")
print(f"Task ID: {task['id']}")
print(f"Task status: {task['status']}")
```

### TypeScript (Server-side)

```typescript
import axios from 'axios';

const BASE_URL = process.env.CHATDOC_STUDIO_BASE_URL || 'https://api.chatdoc.studio/v1';
const API_KEY = process.env.CHATDOC_STUDIO_API_KEY || '';

interface CreateAgentTaskRequest {
  app_id: string;
  upload_ids: string[];
}

interface UploadInfo {
  id: string;
  name: string;
  file_type: string;
}

interface AgentTaskResponse {
  id: string;
  app_id: string;
  status: 'pending' | 'processing' | 'success' | 'failed';
  uploads?: UploadInfo[];
  created_at: number;
  updated_at: number;
  meta: Record<string, unknown>;
}

async function createAgentTask(data: CreateAgentTaskRequest): Promise<AgentTaskResponse> {
  const response = await axios.post<{ data: AgentTaskResponse }>(
    `${BASE_URL}/agent/apps/tasks`,
    data,
    {
      headers: {
        Authorization: `Bearer ${API_KEY}`,
      },
    }
  );
  return response.data.data;
}

const task = await createAgentTask({
  app_id: 'agent_app_xyz',
  upload_ids: ['F1CMSW'],
});

console.log(`Task ID: ${task.id}`);
console.log(`Task status: ${task.status}`);
```

### cURL

```bash
curl -X POST "${CHATDOC_STUDIO_BASE_URL}/agent/apps/tasks" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "agent_app_xyz",
    "upload_ids": ["F1CMSW"]
  }'
```

## Get Task

### Python

```python
def get_agent_task(task_id: str) -> dict:
    """Get Agent App task status."""
    url = f"{BASE_URL}/agent/apps/tasks/{task_id}"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["data"]


task = get_agent_task("task_abc123")
print(f"Status: {task['status']}")
print(f"Meta: {task['meta']}")
```

### TypeScript

```typescript
async function getAgentTask(taskId: string): Promise<AgentTaskResponse> {
  const response = await axios.get<{ data: AgentTaskResponse }>(
    `${BASE_URL}/agent/apps/tasks/${taskId}`,
    {
      headers: {
        Authorization: `Bearer ${API_KEY}`,
      },
    }
  );
  return response.data.data;
}

const task = await getAgentTask('task_abc123');
console.log(`Status: ${task.status}`);
console.log('Meta:', task.meta);
```

### cURL

```bash
curl -X GET "${CHATDOC_STUDIO_BASE_URL}/agent/apps/tasks/task_abc123" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}"
```

## Get Task Result

### Python

```python
def get_agent_task_result(task_id: str) -> str:
    """Get Agent App task result text."""
    url = f"{BASE_URL}/agent/apps/tasks/{task_id}/result"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["data"]


result = get_agent_task_result("task_abc123")
print(result)
```

### TypeScript

```typescript
async function getAgentTaskResult(taskId: string): Promise<string> {
  const response = await axios.get<{ data: string }>(
    `${BASE_URL}/agent/apps/tasks/${taskId}/result`,
    {
      headers: {
        Authorization: `Bearer ${API_KEY}`,
      },
    }
  );
  return response.data.data;
}

const result = await getAgentTaskResult('task_abc123');
console.log(result);
```

### cURL

```bash
curl -X GET "${CHATDOC_STUDIO_BASE_URL}/agent/apps/tasks/task_abc123/result" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}"
```

## Complete Workflow Example

### Python

```python
def wait_for_agent_task(task_id: str, timeout: int = 600, interval: int = 5) -> dict:
    """Poll task status until it finishes."""
    start = time.time()

    while time.time() - start < timeout:
        task = get_agent_task(task_id)
        status = task["status"]

        if status == "success":
            return task
        if status == "failed":
            error = task.get("meta", {}).get("error", "unknown error")
            raise RuntimeError(f"Agent task failed: {error}")

        print(f"Task still running: {status}")
        time.sleep(interval)

    raise TimeoutError("Timed out waiting for Agent task to finish")


task = create_agent_task("agent_app_xyz", "F1CMSW")
wait_for_agent_task(task["id"])
result = get_agent_task_result(task["id"])
print("Final result:")
print(result)
```

### TypeScript

```typescript
async function waitForAgentTask(
  taskId: string,
  timeoutMs = 600_000,
  intervalMs = 5_000
): Promise<AgentTaskResponse> {
  const start = Date.now();

  while (Date.now() - start < timeoutMs) {
    const task = await getAgentTask(taskId);

    if (task.status === 'success') {
      return task;
    }
    if (task.status === 'failed') {
      const error = String(task.meta.error ?? 'unknown error');
      throw new Error(`Agent task failed: ${error}`);
    }

    console.log(`Task still running: ${task.status}`);
    await new Promise(resolve => setTimeout(resolve, intervalMs));
  }

  throw new Error('Timed out waiting for Agent task to finish');
}

const createdTask = await createAgentTask({
  app_id: 'agent_app_xyz',
  upload_ids: ['F1CMSW'],
});

await waitForAgentTask(createdTask.id);
const finalResult = await getAgentTaskResult(createdTask.id);
console.log('Final result:');
console.log(finalResult);
```

### cURL

```bash
# 1. Create task
TASK_ID=$(curl -s -X POST "${CHATDOC_STUDIO_BASE_URL}/agent/apps/tasks" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "agent_app_xyz",
    "upload_ids": ["F1CMSW"]
  }' | jq -r '.data.id')

echo "Created task: ${TASK_ID}"

# 2. Poll until finished
while true; do
  STATUS=$(curl -s -X GET "${CHATDOC_STUDIO_BASE_URL}/agent/apps/tasks/${TASK_ID}" \
    -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}" | jq -r '.data.status')

  echo "Current status: ${STATUS}"

  if [ "${STATUS}" = "success" ]; then
    break
  fi

  if [ "${STATUS}" = "failed" ]; then
    curl -s -X GET "${CHATDOC_STUDIO_BASE_URL}/agent/apps/tasks/${TASK_ID}" \
      -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}" | jq '.data.meta'
    exit 1
  fi

  sleep 5
done

# 3. Fetch final result
curl -X GET "${CHATDOC_STUDIO_BASE_URL}/agent/apps/tasks/${TASK_ID}/result" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}"
```
