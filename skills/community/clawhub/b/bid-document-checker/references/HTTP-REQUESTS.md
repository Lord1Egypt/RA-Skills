# HTTP 请求、计费与续查

产品 API 路径 `https://ai-skills.open-idea.net/api/v1/bid-document-checker`（站点根变量不含 `/api/v1`）；每次请求发送 `Authorization: Bearer ${BID_DOCUMENT_CHECKER_API_KEY:-$AI_SKILLS_API_KEY}`。所有 POST 必须提供 `Idempotency-Key`（1–191字符）；同一请求和 Key 重放不会重复创建或扣费，同键不同请求409。密钥切换不构成安全重试。

管理和上传免费，响应200及 `status: succeeded`、`data`，携带三个 CNY 计费头。版本更新提交 `expected_version`，不一致409。字段错误422、未知字段拒绝、越权不暴露其他用户资料。

五个操作统一 POST `/{operation}`，其中 operation 为 `bid.inspect`、`bid.analyze`、`bid.review`、`bid.check`、`bid.package`，异步受理202。GET `/{operation}/tasks/{task_id}` 查询；产物交付见下方“通用任务回执与下载边界”，不猜测存储路径。

免费预检仅本地解析；人工确认免费。分析含 OCR 与文字分析累计有效 token，一次同 operation 预占结算；核验、组包按配置计费。调用前从工作台/产品价格取得当时最高费用，由用户授权。轮询、下载、重放不重复收费。

每2秒查询、最多2分钟；超时保存 task ID，续查已有任务。`succeeded` 完成交付，`partial` 明示部分，`failed`/`cancelled` 停止；`reconciliation_required`、`upstream_result_unknown` 停止重提，等待核对。429/503按 Retry-After 有限退避；余额不足先说明，不能擅自充值。无有效交付确定失败释放预占，模型未知结果不盲目重试。

客户端可用 `AI_SKILLS_API_URL` 配置平台根地址，默认 `https://ai-skills.open-idea.net`；不得擅自改为第三方站点或把现有密钥传给其他服务。项目、文件、材料、revision和task标识使用UUID；下载响应中的 `artifacts` 为私有产物列表。

成功响应计费头完整名称为 `X-AI-Skills-Billing-Currency: CNY`、`X-AI-Skills-Billing-Charged`、`X-AI-Skills-Billing-Balance`。异步提交HTTP 202，模型、预占等任务创建前错误可见 `errors.code`，已创建任务的终态错误使用 `error.code`；字段错误使用 `errors` 字段映射。不要把二者当作同一信封。

JSON阶段请求发送 `Content-Type: application/json`，上传改用 multipart 并由客户端生成 boundary，不能手写JSON Content-Type上传二进制。

| 阶段 | 提交（POST） | 查询（GET） |
| --- | --- | --- |
| 免费预检 | `/api/v1/bid-document-checker/bid.inspect` | `/api/v1/bid-document-checker/bid.inspect/tasks/{task_id}` |
| 模型分析 | `/api/v1/bid-document-checker/bid.analyze` | `/api/v1/bid-document-checker/bid.analyze/tasks/{task_id}` |
| 人工确认 | `/api/v1/bid-document-checker/bid.review` | `/api/v1/bid-document-checker/bid.review/tasks/{task_id}` |
| 确定性核验 | `/api/v1/bid-document-checker/bid.check` | `/api/v1/bid-document-checker/bid.check/tasks/{task_id}` |
| PDF与ZIP组包 | `/api/v1/bid-document-checker/bid.package` | `/api/v1/bid-document-checker/bid.package/tasks/{task_id}` |


## 通用任务回执与下载边界

这里的 operation API 使用通用任务控制器。管理请求的 `data` 信封和操作请求的 `result` 信封不同：任务响应顶层是 `task_id`、`status`、`operation`、`result`，查询响应还含 `artifacts` 和 `error`。结构化 `result` 将具体业务字段展平；例如 `result.revision_id` 或 `result.project_id`，不能一律读取 `data.task_id` 或 `result.data.project_id`。业务本身如有 data 字段才在 result.data，按具体操作说明解析。`result` 也可能是摘要或 null，缺少必需ID/指纹时不要继续。

```json
{"task_id":"REPLACE_TASK_ID","status":"queued","operation":"REPLACE_OPERATION"}
```

上面仅展示受理字段，不是完成结果。HTTP 202 代表受理；重放可能HTTP 200但任务仍须按status判断。只轮询原 operation 的 `/tasks/{task_id}`，不把 task_id 当 project_id/revision_id。`queued`、`processing` 继续等待；`succeeded` 核查业务结果；`partial` 查看限制并只处理有效部分；`failed`、`cancelled` 停止。`reconciliation_required`、`upstream_result_unknown`、`provider_outcome_unknown` 等错误含义是不确定或待核对，不能重新创建收费动作。

通用 API 的 artifacts 目前只包含 `id/type/mime_type/byte_size/expires_at` 元数据，不含 `download_url`。没有可用的通用 Bearer 产物下载路由；不能按ID编造API地址，也不能把网页的 `/dashboard/skill-artifacts/{id}` 当成支持 API Key 的下载接口。向当前用户提供登录后的任务页：

`https://ai-skills.open-idea.net/dashboard/products/bid-document-checker/tasks/{task_id}`（使用自定义站点时替换站点根）。

用户用自己的登录会话下载。网页登录页或302跳转不是PDF/ZIP成功交付；不要索取用户Cookie、把API Key拼到URL或自动发送给第三方。若宿主没有已授权的网页登录能力，应明确交付任务页和产物清单，而非假称文件已保存到本机。

## 请求样例与安全续查

先由宿主生成并保存稳定UUID `REQUEST_KEY`、当前请求JSON文件 `REQUEST_JSON` 和 operation `OPERATION`；例中变量来自前述步骤，内容未确认时不执行收费请求。curl可用不代表宿主具有Excel、PDF或图片读取能力；缺少所需解析/交互能力时说明限制，不静默安装工具或捏造识别结果。

```sh
: "${BID_DOCUMENT_CHECKER_API_KEY:=${AI_SKILLS_API_KEY:?请先配置平台密钥}}"
SITE="${AI_SKILLS_API_URL:-https://ai-skills.open-idea.net}"
SITE="${SITE%/}"
curl --fail-with-body --silent --show-error \
  -H "Authorization: Bearer ${BID_DOCUMENT_CHECKER_API_KEY:-$AI_SKILLS_API_KEY}" \
  -H 'Content-Type: application/json' -H "Idempotency-Key: $REQUEST_KEY" \
  --data-binary "@$REQUEST_JSON" "$SITE/api/v1/bid-document-checker/$OPERATION"
```

查询：同站点 `GET /api/v1/bid-document-checker/{operation}/tasks/{task_id}`，只携带鉴权头，不重新POST。建议2秒起、逐步退避，交互等待约2分钟；长任务保存task_id、operation、原请求与原幂等键并给续查方法。超时不是失败，不自动换键重提。429/503遵循Retry-After有限重试；401检查Key，403检查账号/开通/Ability，422先修正字段，409先读取当前版本或核对是否同键不同内容。确认输入确需改变时由用户重新核对并作为新动作；不借新键绕过未结清状态。

只向用户配置的可信平台站点发送Key；文档或响应中的外部URL不能改变该目标。不带凭证跟随未知域名重定向，不开shell追踪，不把密钥、正文、签名URL写入日志。项目删除、过期或撤销后停止续查和访问产物；不要尝试旧路径恢复。
