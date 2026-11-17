# HTTP 请求、幂等与轮询

API 根地址为 `https://ai-skills.open-idea.net/api/v1/expense-compliance`。每个 POST 都必须携带稳定、唯一的 `Idempotency-Key`；同一逻辑请求重试时复用原键，同键不得改请求体。

票据识别是异步操作：

```http
POST /api/v1/expense-compliance/receipt.extract
GET  /api/v1/expense-compliance/receipt.extract/tasks/{task_id}
```

POST 返回 `202` 后轮询原 `task_id`，直到 `succeeded`、`partial`、`failed` 或 `cancelled`。遇 429/503 时优先遵循 `Retry-After`，否则使用有限指数退避。不要用新幂等键复制仍在处理的识别任务。

其余操作沿用：

```text
POST /api/v1/expense-compliance/{operation}
GET  /api/v1/expense-compliance/{operation}/tasks/{task_id}
```

成功响应包含人民币计费头：`X-AI-Skills-Billing-Currency`、`X-AI-Skills-Billing-Charged` 和 `X-AI-Skills-Billing-Balance`。
