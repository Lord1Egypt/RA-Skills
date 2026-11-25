---
name: maxaeo-api
description: MaxAEO 开发者平台（开放 API 与 MCP 服务器）的接入指南。当需要写代码调用 MaxAEO 开放 API，向豆包、DeepSeek、Kimi、腾讯元宝等 AI 平台提问并获取回答原文、引用来源与分享链接，处理 ret 错误码、异步任务轮询与点数计费，或配置 MaxAEO 的 MCP 服务器时使用。
---

# MaxAEO 开放 API 接入指南（给 AI 编码助手）

本文件是 MaxAEO 开发者平台文档的浓缩版，供 AI 编码助手在编写接入代码前阅读。与线上文档冲突时，以线上文档为准。

- 完整文档：https://maxaeo.cn/docs/developers/
- 开发者平台全部页面合并成的单个文本文件：https://maxaeo.cn/docs/_llms-txt/developer-platform.txt
- 本文件最新版：https://maxaeo.cn/docs/developers/maxaeo-api.md

## 它能做什么

提交「一个问题 + 一个目标 AI 平台」，MaxAEO 到该平台真实提问，返回 AI 的回答原文（Markdown）、引用来源和分享链接；部分平台还提供执行过程（思考、实际使用的检索词）和多媒体卡片。任务异步执行，只有成功的任务扣点数。

两种接入方式，共用同一个 API Key、点数余额和限流额度：

- **开放 API**：后端服务、脚本、数据管道调用。本文主体。
- **MCP 服务器**：让 Claude Code、Cursor 等 AI 客户端直接调用，见文末「MCP」一节。

**不支持的能力**（不要臆造对应的参数或接口）：

- 一次提交只能是一个平台 + 一个问题；多平台、多问题就多次提交。
- 没有 Webhook 回调，结果只能轮询获取。
- 没有取消任务的接口。
- 不能指定模型，不能开关联网搜索。（思考模式可以开关，见 `/task/submit` 的 `thinking` 参数。）
- 不支持多轮对话，每个任务都是独立的单轮提问。
- 没有官方 SDK，没有沙箱环境。

## 工作方式

1. **API Key**：请用户在开发者控制台 https://maxaeo.cn/developers/ 的「API Key」页创建（完整 Key 只显示一次），并自行设置环境变量 `MAXAEO_API_KEY`。不要让用户把完整 Key 贴进对话，也不要把 Key 写进代码或会提交到仓库的配置文件。
2. **先做免费的连通性检查**：调用 `/platforms/get`，`ret` 为 `1` 说明 Key 可用，同时拿到平台标识与单价。
3. **提交任务会消耗用户的点数**：运行任何会调用 `/task/submit` 的代码前先告诉用户。测试时先用 1 个问题、P2 档。查询类接口免费，失败的任务不扣费。
4. 写完代码后，按「必须遵守的规则」逐条自查。

## 基础信息

| 项目 | 值 |
|---|---|
| Base URL | `https://maxaeo.cn/geoapi/geodata/developer` |
| 鉴权 | 请求头 `Authorization: Bearer <API Key>`。Key 以 `gdev_` 开头，共 48 个字符；只认请求头，放在 URL 或请求体里无效 |
| 方法 | 所有接口都是 `POST` |
| 请求体 | JSON 对象，UTF-8，不超过 64 KiB；没有参数的接口也要传 `{}` |
| 成功响应 | `{"ret": 1, "data": {"ent": {…}}}`，业务数据在 `data.ent` |
| 失败响应 | `{"ret": <错误码>, "msg": "{\"zh\":\"…\",\"en\":\"…\"}"}`，HTTP 状态码仍是 `200` |
| 字段命名 | 请求与响应的外层字段是 snake_case（`task_id`）；`raw_result` 内部是 camelCase（`rawContent`） |
| 时间 | Unix 时间戳（秒），`0` 表示尚未发生；`monitor_date` 为 `YYYY-MM-DD`（北京时间） |

| 接口 | 用途 | 计费 |
|---|---|---|
| `POST /platforms/get` | 平台标识、状态、两档单价、近 24 小时统计 | 免费 |
| `POST /task/submit` | 提交一个问题，返回 `task_id` | 成功的任务扣点数 |
| `POST /task/get` | 按 `task_id` 查询状态与结果 | 免费 |
| `POST /task/key/list` | 列出当前 Key 提交的任务，用于找回 `task_id` 和对账 | 免费 |

调用流程：`/platforms/get` 选平台 → `/task/submit` 提交并**立即保存** `task_id` → 每 15 秒调用一次 `/task/get`，直到终态 → 读取结果。提交结果不明时，用 `/task/key/list` 找回。

## 必须遵守的规则

违反任何一条都会产生 bug，其中一部分会导致重复扣费。

1. **用 `ret` 判断请求成败**，`ret == 1` 才是成功。业务失败时 HTTP 状态码也是 `200`；不要按 HTTP 状态码或 `msg` 文案写逻辑。
2. **直接按 JSON 解析响应体**，不要依赖响应头 `Content-Type`（目前可能是 `text/plain`）。
3. **`msg`、`error_message`、`raw_result.error` 都是 JSON 字符串**，要再解析一次才得到 `{"zh": "…", "en": "…"}`；解析失败时把原文当作提示。
4. **请求体只能包含接口定义的字段。** 多出任何字段（包括 `taskId`、`waitSeconds` 这类拼写错误，或 `api_key`），整个请求返回 `1001`，不会被静默忽略。
5. **提交不是幂等的。** 每次调用 `/task/submit` 都会创建一个新任务，成功后各自扣费，服务端不按问题内容去重。提交时遇到超时、连接中断、非 200 状态码或 `ret == -1`，**不要直接重试**：先调用 `/task/key/list`（`keyword` 传问题的前 256 个字符，`start_time` 设为提交前的时间），找到就继续轮询那个 `task_id`，确认没有再重新提交。例外：HTTP `405`、`404` 说明方法或路径写错，确定没有创建任务。
6. **任务是否结束、是否成功，只看 `status`。** 终态只有 `succeeded`、`failed`、`canceled`。`error_code` 非空不等于失败（`dispatching` 状态下会出现 `dispatch_uncertain`）。
7. **轮询间隔约 15 秒**，查得更勤也只会拿到同一个状态。任务没有服务端截止时间，排队时长没有上限；你自己的业务超时不等于任务失败，保留 `task_id`，之后仍可取回结果。任务多时用一个定时循环批量查询，不要为每个任务起一个阻塞等待。
8. **拿到 `task_id` 立即持久化**，连同提交时间和参数一起保存。
9. **平台列表和单价从 `/platforms/get` 动态获取**，不要写死；跳过 `platform_status` 为 `maintenance` 的平台（提交会返回 `1029`）。
10. **`raw_result` 可能不存在**（排队中、被取消、派发失败的任务没有这个字段）。它内部的零值字段会被省略（`false`、`0`、`""`、空数组都不出现），读取时自行补默认值；`elapsedMs` 是字符串。
11. **`references[].cited` 是三态**：`true` 被正文引用，`false` 搜到但未引用，**字段不存在**表示平台不区分——不能当作 `false`。
12. **忽略不认识的响应字段**，以兼容新增字段；列表为空时可能是 `[]` 也可能是 `null`，统一按空数组处理。
13. **响应可能很大**：`answer`、`result_json`、`raw_result` 是同一份结果的三种形态，单个字段最大可达 8 MiB。HTTP 客户端要留够响应大小和读取超时。
14. **API Key 只在服务端使用**，从环境变量读取。不要在浏览器、小程序、App 里直接调用开放 API。日志里只记录 Key 的前 12 个字符。
15. **每次请求记录接口、`ret`、耗时、`task_id`**，以及响应头 `ipalfish-trace-id`（如有），便于排查问题。
16. **`"thinking": true` 只是请求。** 没有思考开关的平台会按关闭执行，不报错。实际是否开启只看 `raw_result.thinking`（为 `false` 时字段省略）；不要用请求值、任务外层的 `thinking` 或有没有 `thinking` 类型的执行步骤来判断。

## 接口参考

### `POST /platforms/get`：查询平台列表

请求体：`{}`

`data.ent`：

- `platforms`：string[]，平台标识列表，**包含维护中的平台**。
- `items`：数组，与 `platforms` 顺序一致，每一项：

| 字段 | 类型 | 说明 |
|---|---|---|
| `platform` | string | 平台标识，如 `doubao` |
| `region` | string | `domestic` 国内 / `overseas` 海外 |
| `platform_status` | string | `normal` 正常；`degraded` 波动（可以提交，可能更慢或偶发失败）；`maintenance` 维护中（不可提交） |
| `p1_credits` / `p2_credits` | integer | P1、P2 档每次**成功**调用的点数 |
| `has_stats` | boolean | 为 `false` 时 `success_rate`、`p50_duration_seconds` 都是 `0`，不要展示成「成功率 0%」 |
| `success_rate` | number | 近 24 小时成功率，0–1 |
| `p50_duration_seconds` | integer | 近 24 小时成功任务从提交到完成的中位耗时（秒，含排队） |
| `sample_count` | integer | 近 24 小时到达终态的任务数 |
| `stats_updated_at` | integer | 统计计算时间（Unix 秒） |

开发者 API 计费未开通时返回空列表。

### `POST /task/submit`：提交任务

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `platform` | string | 是 | 平台标识，取自 `/platforms/get`，不区分大小写 |
| `query` | string | 是 | 问题。去掉首尾空白后最长 4096 个字符，必须包含可见文字 |
| `priority` | integer | 否 | `1` = P1 优先（先出队，单价高）；`2` = P2 标准（默认，单价低）。不传或传 `0` 按 P2 |
| `thinking` | boolean | 否 | 是否请求平台的思考模式（如 DeepSeek 的深度思考、豆包的专家模式），默认 `false`。必须是 JSON 布尔值，传字符串 `"true"` 返回 `1001`。开启后明显更慢，不加价 |
| `country` | string | 否 | 两位字母国家代码（如 `US`、`JP`），只影响海外平台的抓取出口，不加价。一般不需要传 |
| `monitor_date` | string | 否 | 业务日期 `YYYY-MM-DD`（北京时间），默认当天；只是归档标签，既不是执行时间也不是截止时间。也接受带时区的 RFC 3339 时间 |
| `wait_seconds` | integer | 否 | `0`–`120`，默认 `0`。大于 0 时服务端最多等待这么久，任务到达终态就返回；到时仍未结束则返回当时的状态，**仍需继续轮询**。客户端 HTTP 超时要比它多留 15 秒以上 |

`data.ent` 是任务对象：`status` 为 `queued`，`credits` 为预占的点数，结果字段为空。

P1 和 P2 怎么选：有人在界面上等结果、或下游流程卡在这一步时用 P1；每日批量监控、离线分析用 P2。两档都不承诺排队时长。

思考模式：只在用户明确需要平台以思考模式回答时才传 `"thinking": true`。部分平台没有思考开关（见文末平台快照），会按关闭执行；开启后更容易在 `wait_seconds` 内等不到终态，代码必须能继续轮询。

### `POST /task/get`：查询任务

请求体：`{"task_id": "task_…"}`（最长 64 个字符）。可以查询同一用户用任意 Key、或在控制台在线调试中提交的任务。

`data.ent` 是任务对象，见下节。

### `POST /task/key/list`：任务列表

只列出**当前这个 Key** 提交的任务，按提交时间倒序；列表项不含 `answer`、`result_json`、`share_link`、`raw_result`、`updated_at`。参数全部可选：

| 参数 | 类型 | 说明 |
|---|---|---|
| `page` | integer | 页码，从 1 开始，默认 `1` |
| `page_size` | integer | 默认 `20`，最大 `100` |
| `start_time` | integer | 提交时间下限（Unix 秒，含） |
| `end_time` | integer | 提交时间上限（Unix 秒，不含），须大于 `start_time` |
| `platform` | string | 平台标识 |
| `status` | string | 任务状态，精确匹配；例外：传 `pending` 时同时返回 `queued`、`dispatching`、`pending` 的任务 |
| `keyword` | string | 以 `task_` 开头时按任务 ID 精确匹配，否则按「问题包含该文本」匹配；最长 256 个字符 |

`data.ent`：`total`、`page`、`page_size`、`items`。翻页对账时固定 `end_time`，避免翻页期间新提交的任务导致条目重复。

## 任务对象

外层字段即使为空也会返回（`""`、`0` 或 `false`）：

| 字段 | 类型 | 说明 |
|---|---|---|
| `task_id` | string | `task_` 加一个 UUID |
| `platform` / `query` | string | 平台标识（已转小写）/ 问题（已去掉首尾空白） |
| `status` | string | 见下方状态表 |
| `answer` | string | 回答正文（Markdown），等于 `raw_result.rawContent` |
| `result_json` | string | 原始结果的 JSON 字符串，结构同 `raw_result`，可能包含 `raw_result` 尚未收录的新字段 |
| `share_link` | string | 平台分享链接，可能为空 |
| `error_code` / `error_message` | string | 任务级错误码 / `{"zh","en"}` JSON 字符串 |
| `created_at` / `updated_at` / `started_at` / `finished_at` | integer | Unix 秒。`started_at` 可能为 `0`（未记录），计算耗时用 `finished_at - created_at` |
| `monitor_date` | string | 业务日期 |
| `priority` | integer | 提交时的档位；实际执行档位以 `raw_result.priority` 为准 |
| `country` | string | 请求的出口国家（大写），不代表实际出口 |
| `thinking` | boolean | 提交时**请求**的思考模式；实际模式以 `raw_result.thinking` 为准 |
| `credits` | integer | 未结束：预占点数；`succeeded`：扣除的点数；`failed` / `canceled`：`0` |
| `raw_result` | object | 结构化结果，**只在拿到结果后出现**（成功，或平台执行失败） |

状态流转：

```text
queued → dispatching → pending ⇄ running → succeeded | failed | canceled
```

| `status` | 含义 | 终态 |
|---|---|---|
| `queued` | 已受理，等待派发 | |
| `dispatching` | 正在派发，或正在确认派发结果 | |
| `pending` | 已派发，在平台队列中排队（P2 任务遇到可重试的失败会从 `running` 回到这里） | |
| `running` | 正在向 AI 平台提问 | |
| `succeeded` | 拿到了回答（回答很短、`references` 为空都可能是正常结果） | ✓ |
| `failed` | 失败，原因见 `error_code`，不扣费 | ✓ |
| `canceled` | 被取消，不扣费 | ✓ |

### `raw_result`

沿用 protobuf 的 JSON 编码：字段名是 camelCase，零值字段省略。

| 字段 | 类型 | 说明 |
|---|---|---|
| `success` | boolean | 拿到回答时为 `true`；失败时字段不出现 |
| `rawContent` | string | 回答原文（Markdown）。平台自己的引用标记（如 `[citation:3]`、`【turn0search2】`、`<REF>…</REF>`）和卡片占位符原样保留 |
| `references` | Reference[] | 平台搜到或读过的全部来源，被正文引用的排在前面 |
| `shareLink` | string | 分享链接 |
| `error` | string | 失败说明，`{"zh","en"}` JSON 字符串 |
| `elapsedMs` | string | 执行耗时（毫秒，**字符串**，不含排队） |
| `completedAt` | string | 完成时间，ISO 8601 UTC |
| `priority` | integer | 实际执行的档位，对账以此为准 |
| `thinking` | boolean | 实际是否开启了思考：`true` 为开启；没有开启、平台没有开关或任务失败时不出现 |
| `agentSteps` | AgentStep[] | 执行过程，按发生顺序 |
| `mediaCards` | MediaCard[] | 多媒体卡片，按出现顺序 |
| `taskId`、`platform`、`monitorDate`、`query`、`conversationId`、`messageId` | string | 对照用 |

**Reference**：`rank`（从 1 开始）、`title`、`url`（可能为空或是平台内部 ID，使用前校验是否以 `http://` 或 `https://` 开头）、`snippet`、`source`（站点名）、`domain`（可能为空，需要时从 `url` 解析）、`contentPlatform`、`cited`（三态，见规则 11）、`publishTime`（ISO 8601、`YYYY-MM-DD` 或「1天前」这样的平台原文）、`author`。

**AgentStep**：按 `type` 读取对应字段。`thinking`（多数只在开启思考模式时出现）：`content`、`summary`；`search`：`name`、`queries`（AI 实际使用的检索词）、`results`（`title`、`url`、`siteName`、`snippet`，未必被引用）；`tool`：`name`、`args`。

**MediaCard**：`type`（`image` / `video` / `product` / `ranking` / `other`）、`platformType`、`anchor`（卡片在 `rawContent` 中的占位符原文）、`items`（`title`、`url`、`imageUrl`、`source`、`author`、`duration`、`price`、`rating`、`publishTime`、`description`）。`imageUrl` 通常带签名、会过期，需要留存请尽快转存。

判断引用关系请用 `references` 和 `cited`，不要解析正文里的引用标记：标记格式由各平台决定，随时可能变化。

## 错误码

### 请求级：`ret` 不为 `1`

除 `-1` 外，都发生在创建任务之前：没有创建任务，也不扣点数。

| `ret` | 含义 | 处理 |
|---|---|---|
| `1001` | 参数错误：请求体不是单个 JSON 对象（包括空请求体）、超过 64 KiB、包含未定义字段，或字段值不合法；`msg` 会写明字段 | 修正请求，不要自动重试 |
| `1022` | 开发者 API 计费未开通 | 联系商务，不要重试 |
| `1023` | 可用点数不足 | 提示充值，或改用更便宜的平台 / P2；不要自动重试 |
| `1024` | 同时进行的任务数已达上限 | 没有创建任务，等待后重试是安全的 |
| `1025` | 提交过于频繁 | 没有创建任务，退避后重试是安全的 |
| `1029` | 平台未开放或正在维护 | 重新获取平台列表，换平台 |
| `1030` | API Key 缺失、无效、已停用或已过期（不区分具体原因） | 检查 Key，不要重试 |
| `1031` | 任务不存在，或不属于当前用户 | 检查 `task_id` |
| `1003` | 账户权限异常（少见，例如 Key 所属账户的所有权已转移） | 联系 MaxAEO，不要重试 |
| `-1` | 服务暂时不可用 | 查询类接口按 2、4、8 秒…指数退避重试；**提交任务时按规则 5 先确认是否已创建** |

HTTP `405`（方法不是 `POST`）和 `404`（路径写错）表示请求没有进入业务处理。`502`、`504`、超时、连接中断表示无法确定服务端是否已处理：查询类接口直接重试，提交任务按规则 5 处理。

### 任务级：`status` 为 `failed` 或 `canceled`

失败和取消都不扣点数。按 `error_code` 分支处理：

| `error_code` | 含义 | 处理 |
|---|---|---|
| `crawl_failed` | 平台没有返回有效回答 | 隔一段时间重试，或换平台 |
| `credential_invalid` | 任务派发前，提交它的 Key 已失效 | 用有效 Key 重新提交 |
| `crawler_rejected` | 平台暂不支持或已下线 | 重新获取平台列表，换平台 |
| `crawler_internal_error`、`crawler_submit_failed` | 抓取服务没有受理这个任务 | 稍后重试 |
| `crawler_invalid_request` | 请求参数被抓取服务拒绝 | 检查 `query` 和 `country` 后重新提交 |
| `crawler_method_unavailable`、`crawler_auth_failed` | 服务端配置问题 | 联系 MaxAEO |
| `crawl_canceled` | 任务被取消（`status` 为 `canceled`） | 需要的话重新提交 |
| 表外的值 | — | 按「任务失败、不扣费」处理，并记录 `error_message` |

下面两个值出现在**未结束**的任务上，不代表失败，继续轮询即可：`dispatch_uncertain`（`dispatching` 状态，服务端会自行确认，不会重复派发）、`crawler_query_unavailable`（暂时无法同步执行进度）。

重新提交失败的任务会创建一个新任务，成功后才扣费。

## 限流与配额

| 限制 | 默认值 | 口径 | 超出时 |
|---|---|---|---|
| 同时进行的任务 | 5 | 账户内 `queued`、`dispatching`、`running` 的任务（**不含 `pending`**） | `1024` |
| 每分钟提交次数 | 120 | 账户内最近 60 秒（滚动窗口） | `1025` |
| API Key 数量 | 10 | 账户内未删除的 Key | 控制台无法创建新 Key |

- 只有提交任务计入并发和速率；查询类接口不占用这两项额度，但仍请保持约 15 秒的轮询间隔。
- 同一账户下的所有 Key、MCP 调用和控制台在线调试共享额度与点数余额。实际生效的额度以控制台「用量统计 → 额度与限制」为准。
- 批量提交时在客户端主动节流（例如每 0.6 秒最多提交一个）；遇到 `1024` / `1025` 从 15 秒起逐次加倍退避，再重试同一个问题。

## 计费

- 提交时按该平台、该档位的当前单价**预占**点数，单价在提交时锁定；`succeeded` 时正式扣除，`failed` / `canceled` 时退回。
- 可用余额 = 点数余额 − 进行中任务的预占点数。可用余额不足以支付这次的单价时，提交返回 `1023`，不会透支。
- 指定 `country`、开启 `thinking` 都不加价；查询类接口不收费；控制台在线调试固定按 P1 计价。
- 成本估算：问题数 × 每个问题投放的各平台单价之和（只有成功的任务计费）。
- 首次使用开发者平台（进入控制台或用 API Key 调用任一接口）会自动向个人账户赠送 100 点，永久有效，每个账号一次；更多点数在控制台「充值」页在线购买。

## 参考实现

两份实现逻辑相同：查询类接口退避重试；提交遇到结果未知时先找回、确认没有再提交；轮询到终态后读取回答和引用来源。

### Python（`pip install requests`；不想装依赖可直接用本 skill 的 `scripts/maxaeo.py`，只用标准库）

```python
"""MaxAEO 开放 API 最小客户端：安全提交（避免重复扣费）+ 轮询 + 读取结果。"""
import json
import os
import time

import requests

BASE_URL = "https://maxaeo.cn/geoapi/geodata/developer"
HEADERS = {"Authorization": f"Bearer {os.environ['MAXAEO_API_KEY']}"}
TERMINAL = {"succeeded", "failed", "canceled"}
RETRYABLE = {-1, 1024, 1025}


class MaxAEOError(Exception):
    def __init__(self, ret, msg):
        self.ret = ret
        try:
            self.message = json.loads(msg).get("zh") or msg  # msg 是 {"zh","en"} JSON 字符串
        except (TypeError, ValueError, AttributeError):
            self.message = msg
        super().__init__(f"ret={ret}: {self.message}")


def post(path, body, timeout=30):
    resp = requests.post(BASE_URL + path, headers=HEADERS, json=body, timeout=timeout)
    resp.raise_for_status()
    resp.encoding = "utf-8"  # Content-Type 可能是 text/plain，requests 会误用 ISO-8859-1 解码中文
    data = resp.json()
    if data["ret"] != 1:
        raise MaxAEOError(data["ret"], data.get("msg", ""))
    return data["data"]["ent"]


def read(path, body, retries=4):
    """查询类接口（/platforms/get、/task/get、/task/key/list）：可以安全重试。"""
    for attempt in range(retries + 1):
        try:
            return post(path, body)
        except (requests.RequestException, MaxAEOError) as e:
            retryable = not isinstance(e, MaxAEOError) or e.ret in RETRYABLE
            if not retryable or attempt == retries:
                raise
            time.sleep(2 ** (attempt + 1))


def submit(platform, query, **options):
    """提交任务。结果未知时先找回已创建的任务，确认没有才重新提交。
    options 只能是 priority、thinking、country、monitor_date、wait_seconds。"""
    body = {"platform": platform, "query": query, **options}
    timeout = 30 + options.get("wait_seconds", 0)
    started = int(time.time()) - 60  # 留出时钟误差
    for attempt in range(4):
        try:
            return post("/task/submit", body, timeout=timeout)
        except MaxAEOError as e:
            if e.ret in (1024, 1025):  # 被限流：没有创建任务，等待后重试
                time.sleep(15 * (attempt + 1))
                continue
            if e.ret != -1:
                raise
        except requests.HTTPError as e:
            if e.response.status_code in (404, 405):  # 路径或方法写错，确定没有创建任务
                raise
        except requests.RequestException:
            pass
        # 超时、断连、非 200 或 ret=-1：任务可能已创建，先找回
        found = read("/task/key/list", {
            "keyword": query.strip()[:256], "platform": platform, "start_time": started, "page_size": 5,
        })
        if found["items"]:
            return read("/task/get", {"task_id": found["items"][0]["task_id"]})
    raise RuntimeError("提交多次未成功，请稍后再试")


def wait(task_id, interval=15, timeout=1800):
    """每 15 秒查询一次，直到终态。超过 timeout 返回当时的任务：任务仍在执行，之后可以用 task_id 再查。"""
    deadline = time.time() + timeout
    while True:
        task = read("/task/get", {"task_id": task_id})
        if task["status"] in TERMINAL or time.time() >= deadline:
            return task
        time.sleep(interval)


if __name__ == "__main__":
    platforms = read("/platforms/get", {})
    usable = [p["platform"] for p in platforms["items"] or [] if p["platform_status"] != "maintenance"]
    print("可提交的平台：", usable)

    task = submit("doubao", "适合程序员的机械键盘推荐")  # 会消耗点数
    print("task_id：", task["task_id"])  # 生产代码应在这里持久化 task_id
    task = wait(task["task_id"])

    if task["status"] == "succeeded":
        print(task["answer"])
        for ref in (task.get("raw_result") or {}).get("references", []):
            print(ref.get("rank"), ref.get("cited"), ref.get("title"), ref.get("url"))  # cited 为 None 表示平台不区分
        print("扣除点数：", task["credits"])
    elif task["status"] in TERMINAL:
        print("任务未成功：", task["error_code"], task["error_message"])
    else:
        print("仍在执行，稍后用 task_id 再查：", task["status"])
```

### Node.js（18 及以上，保存为 `.mjs` 文件）

```js
// MaxAEO 开放 API 最小客户端：安全提交（避免重复扣费）+ 轮询 + 读取结果
const BASE_URL = "https://maxaeo.cn/geoapi/geodata/developer";
const headers = {
  Authorization: `Bearer ${process.env.MAXAEO_API_KEY}`,
  "Content-Type": "application/json",
};
const TERMINAL = new Set(["succeeded", "failed", "canceled"]);
const RETRYABLE = new Set([-1, 1024, 1025]);
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

class MaxAEOError extends Error {
  constructor(ret, msg) {
    let message = msg;
    try {
      message = JSON.parse(msg).zh || msg; // msg 是 {"zh","en"} JSON 字符串
    } catch {}
    super(`ret=${ret}: ${message}`);
    this.ret = ret;
  }
}

class HTTPError extends Error {
  constructor(status) {
    super(`HTTP ${status}`);
    this.status = status;
  }
}

async function post(path, body, timeoutMs = 30_000) {
  const resp = await fetch(BASE_URL + path, {
    method: "POST",
    headers,
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(timeoutMs),
  });
  if (!resp.ok) throw new HTTPError(resp.status);
  const data = await resp.json(); // Content-Type 可能是 text/plain，直接按 JSON 解析
  if (data.ret !== 1) throw new MaxAEOError(data.ret, data.msg ?? "");
  return data.data.ent;
}

// 查询类接口（/platforms/get、/task/get、/task/key/list）：可以安全重试
async function read(path, body, retries = 4) {
  for (let attempt = 0; ; attempt++) {
    try {
      return await post(path, body);
    } catch (e) {
      const retryable = !(e instanceof MaxAEOError) || RETRYABLE.has(e.ret);
      if (!retryable || attempt === retries) throw e;
      await sleep(2 ** (attempt + 1) * 1000);
    }
  }
}

// 提交任务。结果未知时先找回已创建的任务，确认没有才重新提交。
// options 只能是 priority、thinking、country、monitor_date、wait_seconds
async function submit(platform, query, options = {}) {
  const body = { platform, query, ...options };
  const timeoutMs = 30_000 + (options.wait_seconds ?? 0) * 1000;
  const started = Math.floor(Date.now() / 1000) - 60; // 留出时钟误差
  for (let attempt = 0; attempt < 4; attempt++) {
    try {
      return await post("/task/submit", body, timeoutMs);
    } catch (e) {
      if (e instanceof MaxAEOError && (e.ret === 1024 || e.ret === 1025)) {
        await sleep(15_000 * (attempt + 1)); // 被限流：没有创建任务，等待后重试
        continue;
      }
      if (e instanceof MaxAEOError && e.ret !== -1) throw e;
      if (e instanceof HTTPError && (e.status === 404 || e.status === 405)) throw e; // 路径或方法写错
    }
    // 超时、断连、非 200 或 ret=-1：任务可能已创建，先找回
    const found = await read("/task/key/list", {
      keyword: Array.from(query.trim()).slice(0, 256).join(""),
      platform,
      start_time: started,
      page_size: 5,
    });
    const items = found.items ?? [];
    if (items.length > 0) return read("/task/get", { task_id: items[0].task_id });
  }
  throw new Error("提交多次未成功，请稍后再试");
}

// 每 15 秒查询一次，直到终态。超过 timeoutMs 返回当时的任务：任务仍在执行，之后可以用 task_id 再查
async function wait(taskId, intervalMs = 15_000, timeoutMs = 30 * 60_000) {
  const deadline = Date.now() + timeoutMs;
  for (;;) {
    const task = await read("/task/get", { task_id: taskId });
    if (TERMINAL.has(task.status) || Date.now() >= deadline) return task;
    await sleep(intervalMs);
  }
}

const platforms = await read("/platforms/get", {});
const usable = (platforms.items ?? []).filter((p) => p.platform_status !== "maintenance").map((p) => p.platform);
console.log("可提交的平台：", usable);

let task = await submit("doubao", "适合程序员的机械键盘推荐"); // 会消耗点数
console.log("task_id：", task.task_id); // 生产代码应在这里持久化 task_id
task = await wait(task.task_id);

if (task.status === "succeeded") {
  console.log(task.answer);
  for (const ref of task.raw_result?.references ?? []) {
    console.log(ref.rank, ref.cited, ref.title, ref.url); // cited 为 undefined 表示平台不区分
  }
  console.log("扣除点数：", task.credits);
} else if (TERMINAL.has(task.status)) {
  console.log("任务未成功：", task.error_code, task.error_message);
} else {
  console.log("仍在执行，稍后用 task_id 再查：", task.status);
}
```

## MCP

| 项目 | 值 |
|---|---|
| 地址 | `https://maxaeo.cn/geoapi/geodata/developer/mcp` |
| 传输 | Streamable HTTP，无状态，只返回 JSON（不使用 SSE） |
| 鉴权 | 请求头 `Authorization: Bearer <API Key>`，不支持 OAuth；Key 无效时返回 HTTP `401` |
| 计费与限流 | 与开放 API 完全相同 |

Claude Code：

```bash
claude mcp add --transport http maxaeo https://maxaeo.cn/geoapi/geodata/developer/mcp \
  --header "Authorization: Bearer $MAXAEO_API_KEY"
```

支持远程 MCP 服务器和自定义请求头的客户端（如 Cursor 的 `mcp.json`）：

```json
{
  "mcpServers": {
    "maxaeo": {
      "url": "https://maxaeo.cn/geoapi/geodata/developer/mcp",
      "headers": { "Authorization": "Bearer gdev_你的完整Key" }
    }
  }
}
```

含 Key 的配置文件不要提交到代码仓库。只支持 stdio 的客户端，可以用 `npx -y mcp-remote https://maxaeo.cn/geoapi/geodata/developer/mcp --header "Authorization:${MAXAEO_AUTH}"` 桥接，并把环境变量 `MAXAEO_AUTH` 设为 `Bearer gdev_…`。

工具的参数名、取值范围与对应接口相同，同样拒绝未定义的字段：

| 工具 | 参数 | 说明 |
|---|---|---|
| `list_platforms` | 无 | 同 `/platforms/get` |
| `submit_task` | `platform`、`query`；可选 `priority`、`thinking`、`country`、`monitor_date`、`wait_seconds` | 每次调用都创建新任务，成功后扣点数 |
| `get_task` | `task_id`；可选 `include_raw` | 默认返回精简摘要：不含 `result_json` 和 `raw_result`，`references` 每项只有 `rank`、`title`、`url`、`domain`、`cited`，空字段省略。`thinking` 是请求的思考模式；`effective_thinking` 是实际模式，拿到结果后才出现（`false` 也返回）。`include_raw: true` 时附带完整 `raw_result` |
| `list_tasks` | 同 `/task/key/list` | 列出当前 Key 提交的任务 |

推荐流程：`list_platforms` → `submit_task` → 反复 `get_task` 直到终态；提交结果不明时先 `list_tasks` 找回，不要重复提交。工具错误以 `isError: true` 返回，文本为 `error <错误码>: <英文提示> (<中文提示>)`，错误码与开放 API 的 `ret` 相同；参数写错时文本为 `invalid arguments: …`。

## 平台标识（快照）

以 `/platforms/get` 的实时返回为准，不要写死在代码里。

- 国内：`doubao` 豆包、`deepseek` DeepSeek、`kimi` Kimi、`yuanbao` 腾讯元宝、`qianwen` 千问、`wenxin` 文心一言、`zhipu` 智谱清言、`xunfei` 讯飞星火、`metaso` 秘塔 AI 搜索、`xiaohongshu` 小红书点点
- 海外：`chatgpt`、`gemini`、`claude`、`perplexity`、`copilot`、`grok`、`google-ai-mode`、`google-ai-overview`

思考开关（2026 年 10 月，平台改版可能变化）：`deepseek`、`doubao`、`kimi`、`yuanbao`、`qianwen`、`zhipu`、`metaso`、`xunfei`、`chatgpt` 有开关；其余平台传 `"thinking": true` 也按关闭执行。DeepSeek 正文的引用标记随之变化：关闭时为 `[citation:N]`，开启时为 `[reference:N]`。

`cited` 的支持情况（观测结果，平台改版可能变化）：豆包、Kimi、腾讯元宝、智谱清言、秘塔 AI 搜索、文心一言区分 `true` / `false`；DeepSeek 只对能对应到具体网页的来源标 `true`，其余不设；讯飞星火恒为 `true`；千问、小红书点点和海外平台不设。

## 更多文档

- 快速开始：https://maxaeo.cn/docs/developers/quickstart/
- 认证与 API Key：https://maxaeo.cn/docs/developers/authentication/
- API 概述：https://maxaeo.cn/docs/developers/api/
- 任务对象：https://maxaeo.cn/docs/developers/api/task-object/
- 任务生命周期：https://maxaeo.cn/docs/developers/guides/task-lifecycle/
- 解析回答结果：https://maxaeo.cn/docs/developers/guides/results/
- 错误处理：https://maxaeo.cn/docs/developers/guides/errors/
- 限流与配额：https://maxaeo.cn/docs/developers/guides/rate-limits/
- 计费与点数：https://maxaeo.cn/docs/developers/guides/billing/
- 上线检查清单：https://maxaeo.cn/docs/developers/guides/production-checklist/
- 接入 MCP：https://maxaeo.cn/docs/developers/mcp/
- MCP 工具参考：https://maxaeo.cn/docs/developers/mcp/tools/
- 常见问题：https://maxaeo.cn/docs/developers/faq/
