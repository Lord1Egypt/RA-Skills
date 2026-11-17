# 操作字段与最小流程

所有主操作 POST 均为 JSON，加平台 Bearer 与独立稳定 Idempotency-Key；上传除外。此处尖括号均为待替换的真实服务端 ID，示例数字只是演示，不能当作实际版本。先参照 HTTP-REQUESTS 建课上传并读取回执。讲稿、术语表均可选。

## 选择输入路径

已有 SRT/VTT：上传 `purpose=subtitle` → inspect → proofread → 人工 review → export，跳过收费 transcribe。仅有字幕也能校对和导出，但没有媒体不核验音频同步、媒体边界或试听；同时上传媒体可检查时长与边界，仍不能把导入字幕视为已音频对齐。

只有媒体：上传 `purpose=media` → inspect → 用户确认音轨、核验时长、费用和传输范围 → transcribe → proofread → 人工 review → export。转写不是普通字幕校对的必经步骤。用户已有字幕而另行要求重新识别时，明确作为新的付费需求取得授权。

## 检查已有字幕或媒体

POST `/api/v1/course-subtitle/subtitle.inspect`，已有字幕的最小请求：

```json
{"project_id":"<创建返回的data.project_id>","expected_version":1,"subtitle_file_id":"<字幕上传返回的data.file_id>"}
```

只有媒体则将 `subtitle_file_id` 替换为 `media_file_id`。可同时传二者，可选 `script_file_id`、`terms_file_id` 和 `audio_stream_index`。从 GET 项目的 `data.version` 取当前版本；多音轨由用户确认索引。

从任务回执取顶层 `task_id` 并轮询；完成后取 `result.project_version`，已有字幕还取 `result.revision_id`。媒体分支返回 `result.media`（含核验时长、计费秒数、音轨与转换偏移）；不能从文件名估算时长。读取 `issues`、`limitations`、`audio_alignment_verified`；无字幕时 revision_id 为空，不能直接校对。

## 按授权转写媒体

POST `/api/v1/course-subtitle/subtitle.transcribe`：

```json
{"inspect_task_id":"<成功媒体inspect的task_id>"}
```

只引用当前用户有效、含媒体的 inspect 回执。服务端从预检快照冻结项目版本与 `billing_units`，客户端不填这些隐藏计费字段，也不构造上游任务 ID。付费前要求用户确认冻结媒体/音轨、`media.billing_seconds`、当前价格及数据传输范围。

轮询原任务直到明确完成。从 `result.revision_id`、`result.project_version` 取后续字幕版本；检查 `zero_speech`、`cue_count`、`issues`。零语音成功仍收费，不虚构字幕补齐空结果。转写返回的时间戳是语音证据，文字与同步仍需人工核对。遇未知上游结果不新建 transcribe。

## 规则或模型校对

POST `/api/v1/course-subtitle/subtitle.proofread`，免费最小路径：

```json
{"revision_id":"<inspect或transcribe返回的revision_id>","expected_version":2,"mode":"rules_only"}
```

`expected_version` 来自该回执的 `result.project_version` 并与 GET 项目核对。`rules_only` 免费、零 Token，提供确定性术语与可读性检查，正常任务状态为 `partial`，不代表完成了模型文字校对。请求 `model` 模式前取得付费授权；省略 mode 默认 model，因此不要为免费检查省略它。模型文字载荷上限 200000 字符，超限让用户选择按课时拆分或 rules_only。

完成后保存校对 `task_id`、`result.project_version`、`result.revision_id`、`result.suggestions`、`result.script_differences`、`result.issues`、`result.limitations`。建议里的 `id/cue_id/original/replacement/reason/cue_original` 都来自实际回执；Agent 不能编造建议 ID。讲稿顺序匹配差异只是候选，不能断言漏讲、错讲或删除增讲。

结构化结果可能被通用安全展示上限截断（如 `_truncated` 或 `_meta.truncated`）；不完整的建议清单不能当全量人工确认依据。停止全量确认声明，引导用户在工作台核对；当前公共 API 不提供完整建议分页接口。

## 逐项人工确认

POST `/api/v1/course-subtitle/subtitle.review`：

```json
{"proofread_task_id":"<校对task_id>","expected_version":2,"decisions":[{"suggestion_id":"<用户已逐条确认的建议id>","accept":true}]}
```

`accept` 必须是用户对该建议明确作出的布尔决定。拒绝传 `false`；未决定不补填，不用全选代签。若实际没有建议，最小 `decisions: []` 合法；有建议时空数组会保留未决草稿。不能因为示例写 true 就执行接受。

可选字段：

- `edits: [{"cue_id":"<真实句段ID>","text":"<用户确认的新文字>"}]`：仅人工改字，保留原句段时间。
- `splits: [{"cue_id":"<真实句段ID>","after_word_ids":["<已有字词锚点ID>"]}]`：仅使用已有可靠、非末尾字词时间锚点，不插值、不自建 ID；改字后无法与原词序可靠映射的句段不能拆分。
- `acknowledgements: [{"cue_id":"<真实句段ID>","code":"<实际提示code>","reason":"<用户确认的理由>"}]`：仅接受真实非阻断提示；结构阻断错误不能豁免。

提交前逐条展示修改及影响，保留用户决定，不自行补签理由。项目版本或术语改变时旧建议失效，读取新版本，必要时重新校对并取得授权。

review 的任务 `succeeded` 只表示写入新修订；从 `result.revision_id`、`result.project_version` 取新回执。只有 `result.status: confirmed` 才是确认版；`draft`、`pending_suggestions: true` 或 `unresolved_issues` 表示尚有未决事项。不能把任务成功冒充人工确认完成。

## 导出与交付

POST `/api/v1/course-subtitle/subtitle.export`：

```json
{"revision_id":"<review返回的result.revision_id>"}
```

导出免费，输出私有 SRT、VTT、`proofread-report.json`。从原导出任务读取 `result.status`、`result.report` 和顶层 `artifacts` 元数据。draft 可导出但必须明确“待确认草稿”，报告包含问题和覆盖限制；负时间、倒序或媒体越界会阻止导出，先修复，不能改写状态绕过校验。

当前公共 API 不返回导出下载地址；交付工作台登录下载入口与 artifact 元数据，不伪造文件或下载成功。报告用户实际费用、确认状态、剩余提示、同步证据和有效期，不自动发布、外传或上传其它系统。
