# HTTP 请求、幂等与任务轮询

令 `BASE=${AI_SKILLS_API_URL:-https://ai-skills.open-idea.net/api/v1}`。每个不同业务动作生成一个 UUID 作为 `Idempotency-Key`；网络结果不确定时只重放完全相同的操作、请求体与键。冲突或 `errors.idempotency_key` 表示请求形状或键不合法，不要改请求体后复用旧键。

四个 POST 入口及对应任务入口：

- `/api/v1/business-documents/document.create`；`/api/v1/business-documents/document.create/tasks/{task_id}`
- `/api/v1/business-documents/document.read`；`/api/v1/business-documents/document.read/tasks/{task_id}`
- `/api/v1/business-documents/document.update`；`/api/v1/business-documents/document.update/tasks/{task_id}`
- `/api/v1/business-documents/document.export`；`/api/v1/business-documents/document.export/tasks/{task_id}`

请求示意：

```sh
curl -sS -X POST "$BASE/business-documents/document.read" \
  -H "Authorization: Bearer ${BUSINESS_DOCUMENTS_API_KEY:-$AI_SKILLS_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: $REQUEST_UUID" \
  --data '{"document_id":"实际 UUID"}'
```

`200` 表示已完成，`202` 表示已接收。收到 `202` 后按响应中的任务 ID 轮询对应 `/tasks/{task_id}`，采用 1、2、4、8 秒有上限退避，最长约 60 秒；持续运行时告知用户稍后重试，不能重复创建。终态为 `succeeded`（成功）、`partial`（部分成功）或 `failed`（失败）。读取结构化结果及 `artifacts` 字段；下载链接只交给当前用户。

保留并解析 `X-AI-Skills-Billing-Currency`、`X-AI-Skills-Billing-Charged`、`X-AI-Skills-Billing-Balance`。错误优先读取 `errors.code`，兼容读取 `error.code`。
