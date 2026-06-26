---
name: bailian-subagent
description: Spawn a bailian (百炼 DashScope) subagent to handle token-heavy or compute-intensive tasks. Use when the main agent needs to delegate data processing, batch operations, DataWorks/MaxCompute SQL execution, news fetching, or any task where saving Claude tokens matters. Triggers on phrases like "讓百炼做", "丟給百炼", "省token", "subagent去做", "delegate to bailian", or when a task is large/repetitive enough to warrant offloading.
---

# Bailian Subagent

Delegate heavy tasks to a cheaper bailian model to save Claude tokens.

## Available Models

| Model | Use case |
|-------|----------|
| `bailian/qwen3.5-plus` | General tasks, data processing, writing |
| `bailian/qwen3-coder-plus` | Code generation, debugging, scripts |
| `bailian/kimi-k2.5` | Long context, document analysis |
| `bailian/glm-5` | Alternative general model |

Default recommendation: `bailian/qwen3.5-plus` for most tasks.

## How to Spawn

```
sessions_spawn(
    task="<detailed instructions>",
    model="bailian/qwen3.5-plus",
    runtime="subagent",
    mode="run",
    runTimeoutSeconds=600
)
```

## What to Delegate

**Good candidates:**
- DataWorks / MaxCompute SQL execution (DROP/CREATE/INSERT/SELECT)
- Batch data processing or transformation
- Fetching and summarizing news / RSS feeds
- Writing boilerplate code or scripts
- Long document analysis or summarization
- Any task with large context or repetitive steps

**Keep with Claude (main agent):**
- Final decisions and trading advice
- Conversation with Samuel
- Tasks requiring memory/context of prior sessions
- Sensitive judgment calls

## Writing Good Task Instructions

Include all required context in the task string — subagent starts fresh with no memory:
- Credentials / endpoints (if needed)
- Exact steps to follow
- Expected output format
- Error handling instructions

## DataWorks Pattern (verified)

When delegating MC/DW SQL tasks, provide this pattern in the task:

```python
from alibabacloud_dataworks_public20240518.client import Client
from alibabacloud_dataworks_public20240518 import models as dw_models
from alibabacloud_tea_openapi.models import Config
import uuid, time

config = Config(
    access_key_id='${ALICLOUD_ACCESS_KEY_ID}',
    access_key_secret='${ALICLOUD_ACCESS_KEY_SECRET}',
    endpoint='dataworks.cn-hangzhou.aliyuncs.com',
    region_id='cn-hangzhou'
)
client = Client(config)
# ... run_sql() helper pattern
```

Key params: project_id=579810, owner=1206989323863181, resource_group_id=Serverless_res_group_421503158374466_777119112505568, datasource=samuelhsin

Sleep 15s between SQL calls to avoid throttling.
