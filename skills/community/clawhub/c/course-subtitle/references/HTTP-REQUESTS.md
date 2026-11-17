# 请求、上传与轮询

## 地址和认证

站点根地址 `${AI_SKILLS_API_URL:-https://ai-skills.open-idea.net}` 不带 `/api/v1`。所有下述公共 API 带 `Authorization: Bearer ${COURSE_SUBTITLE_API_KEY:-${AI_SKILLS_API_KEY}}`，缺少两个 Key 时停止。JSON 请求带 `Content-Type: application/json`，上传让客户端生成 multipart boundary。每个 POST 都带稳定、独立的 `Idempotency-Key`（建议 UUID，最多 191 字符），保存请求、Key 标识和回执供恢复；不要保存密钥正文。

下面是结构示例，不是本次任务的真实回执。尖括号值必须替换为当前用户此前响应的真实 ID，版本数字必须替换为实际返回值；不得根据示例拼接或猜测回执。主任务 JSON 见 OPERATIONS。

## 建课与上传

POST `/api/v1/course-subtitle/projects`：

```json
{"name":"第一课"}
```

同步返回 `data.project_id`、`data.version`（新建为 1）、`data.expires_at` 等项目详情；这是普通管理响应，没有 `task_id`。讲稿与术语可省略。创建也支持可选 `script` 文字、`terms` 数组（`standard`、`aliases`）和 `rules`，不要为了普通校对要求用户准备这些材料。

POST `/api/v1/course-subtitle/projects/{project_id}/files` 必须 multipart，不能发送文件路径 JSON：

```text
purpose=subtitle
file=@/用户已授权的路径/lesson.srt
```

`purpose` 为 `media/subtitle/script/terms`；返回 `data.file_id`、`data.purpose`、`data.byte_size`、`data.expires_at`。上传不等于 inspect。每个文件各用一个独立幂等键；相同上传重放保持文件内容、用途、扩展名不变。

支持媒体 MP3/M4A/WAV/MP4，单个最多 256 MiB、媒体最多 7200 秒；字幕 SRT/VTT、讲稿 TXT/DOCX、术语 TXT，单附件最多 10 MiB。文本为 UTF-8；最多 10000 条字幕、讲稿 120000 字符、500 条术语。术语 TXT 每行 `标准词|别名1|别名2`。多音轨 inspect 必须提供用户选定的 `audio_stream_index`，不得猜选。超限先告知用户按课时拆分，不能自动制造多笔付费任务。

GET `/api/v1/course-subtitle/projects/{project_id}` 返回 `data.version`、`data.files`、`data.revisions` 等，用于读取当前项目与字幕。POST 同一路径可更新 `expected_version` 和 `name/script/terms/rules`，会改变项目版本，旧授权与建议需重新核对。版本不是本地自增值，始终从服务端读取。

## 主任务与回执

| 操作 POST 路径 | 对应 GET 轮询路径 |
| --- | --- |
| `/api/v1/course-subtitle/subtitle.inspect` | `/api/v1/course-subtitle/subtitle.inspect/tasks/{task_id}` |
| `/api/v1/course-subtitle/subtitle.transcribe` | `/api/v1/course-subtitle/subtitle.transcribe/tasks/{task_id}` |
| `/api/v1/course-subtitle/subtitle.proofread` | `/api/v1/course-subtitle/subtitle.proofread/tasks/{task_id}` |
| `/api/v1/course-subtitle/subtitle.review` | `/api/v1/course-subtitle/subtitle.review/tasks/{task_id}` |
| `/api/v1/course-subtitle/subtitle.export` | `/api/v1/course-subtitle/subtitle.export/tasks/{task_id}` |

各 POST 通常异步返回 202，用回执顶层 `task_id` 查询对应操作。200 也必须检查 `status` 和 `error`，不能只看 HTTP 状态。任务响应结构示意：

```json
{"task_id":"<原任务ID>","status":"succeeded","operation":"subtitle.inspect","result":{"version":1,"summary":"媒体与附件检查完成。","project_id":"<项目ID>","project_version":2,"revision_id":"<导入字幕修订ID>"},"artifacts":[],"error":null}
```

公共任务结果把业务字段展开到 `result` 根，读取 `result.project_version`、`result.revision_id`、`result.suggestions`，不是 `result.data.*`；`result.version` 是结果格式版本，不能用作项目 `expected_version`。管理接口则读取 `data.*`，二者不要混用。

`queued/processing` 继续查询；`succeeded` 完成；`partial` 读取能力限制后决定后续，rules_only 的正常校对结果就是 partial，可被 review 引用。`failed/cancelled` 停止依赖操作。错误码 `reconciliation_required` 或上游结果未知 保持原任务并交平台核对，不能当成功、失败或退款证明。

长 ASR 在平台内部轮询上游（默认间隔 30 秒）；客户端可约 30 秒查询一次并对限流退避。不要再次提交 transcribe 来“继续”，也不要直接调用上游。网络超时而有任务 ID 时先 GET；尚未收到 ID 时仅允许原 API Key、同幂等键、完全相同 POST 恢复回执。持久保存任务状态供跨会话恢复，不把等待时间长当作新收费授权。

任务创建前错误可能是 `status: validation_failed` 与 `errors`，余额看 `errors.balance`，通用幂等冲突看 `errors.idempotency_key`，Provider 错误看 `errors.code`；已创建任务错误看 `error.code`。项目管理还会返回 `error.code: version_conflict/idempotency_key_reused/invalid_request`。409 时先读取当前状态与差异，不能只换键重试；版本或材料变化后取得新授权并创建明确的新操作。

## 私有产物与试听

导出任务的 `artifacts[]` 仅含 `id/type/mime_type/byte_size/expires_at`，没有 `download_url`。当前没有通用 Bearer 产物下载路由，不拼接 API 下载地址、存储键或签名 URL。引导当前用户登录工作台任务页 `https://ai-skills.open-idea.net/dashboard/products/course-subtitle/tasks/{task_id}` 下载 SRT、VTT、报告；该页面依赖用户登录会话，API Key 不能替代。无法在 Agent 中直接下载时明确交付此限制，不声称文件已落到本机。

媒体试听另有 POST `/api/v1/course-subtitle/projects/{project_id}/files/{file_id}/audition`，返回 `data.url` 短期可撤销授权；只对当前用户使用，不记录令牌或转发链接。它是媒体播放授权，不是导出产物下载接口。

## 批次、取消和删除

GET/POST `/api/v1/course-subtitle/batches`；创建最小 JSON 为 `{"name":"第一章"}`，从 `data.batch_id` 取 ID，建课时带 `batch_id`。每批最多 20 课时、2 GiB；账号最多 100 个项目、5 GiB。POST `batches/{batch_id}` 带 `expected_version` 与要改的 `name/terms/rules/status`；批次术语变更只影响新建课时。POST `batches/{batch_id}/delete` 使用 `{}` 删除批次及课时。

POST `projects/{project_id}/cancel`、`projects/{project_id}/delete` 使用 `{}`。取消返回 `data.status` 及在途核对提示；停止新任务，不保证在途任务无费用。批次逐课时记录项目、任务、幂等键、版本和账单，不能把单课失败变成整批重提。删除、试听和批次管理同样需独立稳定幂等键，保留账务核对所需的最少记录。
