# 上传、请求与轮询

## 地址、鉴权与稳定请求

`AI_SKILLS_API_URL` 为站点根地址，不含 `/api/v1`。以下 shell 例子在本机执行，不打印密钥；只使用平台产品 Key 或通用 Key，不配置上游凭证。

```sh
BASE="${AI_SKILLS_API_URL:-https://ai-skills.open-idea.net}"
BASE="${BASE%/}"
: "${DOCUMENT_REDACTION_API_KEY:-${AI_SKILLS_API_KEY:?请先配置平台 Key}}"
# CREATE_KEY 为本次创建意图生成并保存的 UUID；重试沿用它。
curl -sS -X POST "$BASE/api/v1/document-redaction/projects" \
  -H "Authorization: Bearer ${DOCUMENT_REDACTION_API_KEY:-${AI_SKILLS_API_KEY}}" \
  -H "Idempotency-Key: $CREATE_KEY" -H 'Content-Type: application/json' -d '{}'
```

创建同步回执是 `{"data":{"public_id":"<项目 UUID>","version":0,"expires_at":"<时间>"}}`，保存 `data.public_id` 为 `PROJECT_ID`；不要读不存在的 `data.project_id`。随后 `GET /api/v1/document-redaction/projects/{project_id}` 返回 `data.project_id`、`data.version`、`data.expires_at`、`data.state`。这些都是管理回执，不含 `task_id`。

逐个上传真实二进制文件，每次上传前先 GET 当前项目版本；不要并发上传后猜版本。`UPLOAD_VERSION` 来自刚读到的 `data.version`，`UPLOAD_KEY` 为该文件上传意图的稳定 UUID。

```sh
curl -sS -X POST "$BASE/api/v1/document-redaction/projects/$PROJECT_ID/files" \
  -H "Authorization: Bearer ${DOCUMENT_REDACTION_API_KEY:-${AI_SKILLS_API_KEY}}" \
  -H "Idempotency-Key: $UPLOAD_KEY" \
  -F "expected_version=$UPLOAD_VERSION" -F 'file=@/absolute/path/source.pdf'
```

上传回执 `{"data":{"file_id":"<文件 UUID>","version":1}}`；`file_id` 不是任务 ID。新建项目初始版本是 0，首次上传后才能用版本至少为 1 的操作请求。上传不手设 multipart Content-Type。只接受 PDF/JPG/PNG，单文件最多 10 MiB，项目最多 20 文件、合计 100 MiB、100 页；OCR 每任务最多 50 页。

## 操作提交和续查

六项操作均为异步 POST `/api/v1/document-redaction/{operation}`，`operation` 为 `redact.inspect`、`redact.locate`、`redact.analyze`、`redact.review`、`redact.generate`、`redact.export`。各操作的具体路径如下：

| POST | GET 任务 |
| --- | --- |
| `/api/v1/document-redaction/redact.inspect` | `/api/v1/document-redaction/redact.inspect/tasks/{task_id}` |
| `/api/v1/document-redaction/redact.locate` | `/api/v1/document-redaction/redact.locate/tasks/{task_id}` |
| `/api/v1/document-redaction/redact.analyze` | `/api/v1/document-redaction/redact.analyze/tasks/{task_id}` |
| `/api/v1/document-redaction/redact.review` | `/api/v1/document-redaction/redact.review/tasks/{task_id}` |
| `/api/v1/document-redaction/redact.generate` | `/api/v1/document-redaction/redact.generate/tasks/{task_id}` |
| `/api/v1/document-redaction/redact.export` | `/api/v1/document-redaction/redact.export/tasks/{task_id}` |

按 OPERATIONS 中的实际字段生成私有 `request.json`，每项独立生成并保存稳定 UUID `OPERATION_KEY`：

```sh
curl -sS -X POST "$BASE/api/v1/document-redaction/$OPERATION" \
  -H "Authorization: Bearer ${DOCUMENT_REDACTION_API_KEY:-${AI_SKILLS_API_KEY}}" \
  -H "Idempotency-Key: $OPERATION_KEY" -H 'Content-Type: application/json' \
  --data-binary @request.json
curl -sS "$BASE/api/v1/document-redaction/$OPERATION/tasks/$TASK_ID" \
  -H "Authorization: Bearer ${DOCUMENT_REDACTION_API_KEY:-${AI_SKILLS_API_KEY}}"
```

POST 202 仅表示接收，保存 `task_id`，持续查询同 operation 的 GET `/tasks/{task_id}`。查询外层为 `task_id/status/operation/result/artifacts/error`。当前实现的结构化结果将业务字段展开在 `result`：例如 `result.project_version`、`result.revision_id`、`result.confirmation_fingerprint`，不是管理回执的 `data.version`，也不是 `result.data.project_version`；旧任务的 result 可能只是摘要，缺关键字段时重新 GET 项目，不从摘要猜值。异步提交可能省略 `result/artifacts/error`，应以查询为准。

`queued/processing/pending/reconciling` 均不可当成完成；`reconciling` 或 `reconciliation_required/provider_result_unknown/provider_outcome_unknown` 表示需续查或平台对账，不是成功或允许重新提交。仅 `succeeded` 继续下一步；`partial`、`failed`、`cancelled` 停止自动交付并展示错误/限制。检查 `error.code`、`errors.code` 以及 `errors` 字段校验（如 `errors.idempotency_key`），409 冲突时不盲目更换键。

所有 POST/DELETE 使用稳定 `Idempotency-Key`；同键不同请求冲突。同一意图重试必须沿用原键、原路径、原参数和原 expected_version，不能把最新版本改进旧请求。超时已有 task_id 则续查；未收到 task_id 时只以同键同请求恢复原任务，不另开付费任务。确认原任务失败且明确重新执行时才是新的意图，重新取版本与收费授权。项目内容修改或版本冲突，先读取当前项目、展示变化并重新复核。

## 预览、管理与交付边界

GET/POST `/api/v1/document-redaction/projects` 列表/创建；GET/DELETE `/projects/{project}` 查看/删除；DELETE `/projects/{project}/files/{file}` 请求含 `expected_version`。GET `/projects/{project}/pages/{page}` 是本人 Bearer 授权私有 PNG 预览，应实际读取并向用户展示，不向外公开 Key 或链接。页 ID、尺寸、候选位置均从项目 `data.state` 读取。

规则模板 GET/POST `/api/v1/document-redaction/templates`，DELETE `/templates/{template}`；保存模板需要 `name`、`rules`，保存关键词必须明确 `save_sensitive=true`，不得默认长期保存客户词表。

`artifacts` 仅返回 `id/type/mime_type/byte_size/expires_at` 元数据，没有 `download_url`，当前没有通用公开 Bearer API 产物下载路由。`redact.export` 成功也不返回可拼接的下载链接。向用户说明已生成/导出的任务 ID，登录 `https://ai-skills.open-idea.net/dashboard/products/document-redaction` 进入 `/dashboard/products/document-redaction/tasks/{task_id}` 下载对应任务产物；若尚未实际取得文件，不能声称已下载交付。不得公开 S3 路径、原件、预览、原名或映射。项目自创建起保留 7 天，删除/到期后停止引用及下载，不能用旧链接恢复。
