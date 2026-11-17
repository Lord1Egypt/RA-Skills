# dealcenter MCP 工具契约速查

通道：MCP 工具（`dealcenter.*`，19 个），凭据由宿主注入，skill 不管 token/tenant。

## 工具清单（19 个）

### account（4）
| 工具 | 用途 | — |
|---|---|---|
| `dealcenter.account.get_full` | 客户详情（聚合档案） | —|
| `dealcenter.account.list_full` | 列出客户 | —|
| `dealcenter.account.search` | 搜索客户（跨实体召回，matched 按 accounts/contacts/deals 分组） | —|
| `dealcenter.account.create` | 创建客户（同名返现有，不更新字段） | —|

### contact（4）
| 工具 | 用途 | — |
|---|---|---|
| `dealcenter.contact.get_full` | 联系人详情 | —|
| `dealcenter.contact.list_full` | 列出联系人 | —|
| `dealcenter.contact.search` | 搜索联系人（参数名 `query`，非 `q`） | —|
| `dealcenter.contact.upsert` | 创建/更新联系人 | —|

### deal（5）
| 工具 | 用途 | — |
|---|---|---|
| `dealcenter.deal.get_full` | 商机详情（聚合） | —|
| `dealcenter.deal.list_full` | 列出商机 | —|
| `dealcenter.deal.search` | 搜索商机（无 account_id 参数，客户端按客户过滤结果） | —|
| `dealcenter.deal.upsert` | 创建/更新商机 | —|
| `dealcenter.deal.advance` | 推进商机阶段 | —|

### doc（3）
| 工具 | 用途 | — |
|---|---|---|
| `dealcenter.doc.get_full` | 文档详情 | —|
| `dealcenter.doc.list_full` | 列出文档（参数 account_id） | —|
| `dealcenter.doc.create` | 创建文档 | —|

### activity（3）
| 工具 | 用途 | — |
|---|---|---|
| `dealcenter.activity.get` | 获取活动 | —|
| `dealcenter.activity.list_recent` | 最近活动 | —|
| `dealcenter.activity.batch_create` | 批量创建活动 | —|

## 写入字段契约（逐字，不要自由发挥）

### activity（batch_create，单批 ≤100）
```json
{ "account_id": 1, "deal_id": 9, "contact_id": 5,
  "type": "跟进",              // 自由文本 1-32 字，简短中文动作词：跟进/会议/演示
  "happened_at": "2026-09-04T14:30:00+08:00",   // ISO-8601；计划性时间（"下周跟进"）不作 happened_at，写进 summary
  "summary": "与张三开会聊外卖合作进展",
  "sources": [ /* 见下 */ ] }
```

### contact（upsert）
```json
{ "account_id": 1, "name": "张三",
  "contact_methods": [{ "type": "phone", "value": "138xxxx" }],  // ≥1 条，type ∈ phone/email/wechat/other
  "sources": [ /* 见下 */ ] }
```
- 无真实联系方式 → 该联系人挂起（pending），不造假值占位。

### deal（upsert）
```json
{ "account_id": 1, "name": "外卖合作", "stage": "discovery", "sources": [ /* 见下 */ ] }
```
- stage 枚举：`discovery / qualification / proposal / negotiation / closing / success / lost / paused`，未提及默认 discovery。
- name 创建后只读（RENAME_NOT_ALLOWED），不改名绕过。

### account（create）
```json
{ "name": "美团", "sources": [ /* 见下 */ ] }
```
- 幂等：同名返回现有记录（不更新任何字段）；更新已有客户走 hub PATCH（本网关未暴露，不归 skill 管）。

### doc（create）
```json
{ "account_id": 1, "deal_id": 9, "title": "客户邮件", "type": "会话",
  "content": "# 正文 markdown", "sources": [ /* 见下 */ ] }
```
- `type` 值集（hub 服务端强校验，值集外 4xx）：`概况 / 会话 / 调研 / 方案 / 复盘 / 其他`。注意「纪要」是 **activity** 的 type，不在 doc 值集内。
- `content | file_uri` 二选一（双传/双缺 4xx）。**默认走 content 代写路径**：只传 Markdown 文本，服务端落存储后生成并返回 file_uri。
- `file_uri` 仅接受本服务返回的 OSS 对象地址（客户端自造 URI 必被拒）且 1-512 字符；判重按 file_uri（title 不作判重键）。

### sources（所有写入必填非空）
```json
[{ "kind": "chat_turn",          // 输入类型：chat_turn / file_excerpt
   "title": "用户原话前 80 字",
   "url": null,
   "quote": "用户确认的那句原话（verbatim）",
   "occurred_at": "2026-09-04T14:30:00+08:00" }]
```

## 错误码处置

| 响应 | 含义 | 动作 |
|---|---|---|
| DUPLICATE_ACTIVITY_HINT（批量响应内嵌 rejected） | 活动已存在 | 记 reused，不重试不追问 |
| 409 DUPLICATE_FILE_URI | 文档已存在 | 记 reused |
| 409 AMBIGUOUS | 同名候选 ≥2 | 写入侧：自判，判不出问用户 |
| 422 RENAME_NOT_ALLOWED | name 创建后只读 | 不改名绕过 |
| 404 REFERENCE_NOT_FOUND | 挂靠 id 不存在 | 查前置步骤，不硬建 |
| 400 MISSING_REQUIRED_FIELD | 缺必填 | 挂起该项，不造假值 |

## 当前故障面

| 故障 | 影响 | 降级 |
|---|---|---|
| 写入被网关包装为「上游服务拒绝了本次请求」，看不到具体 4xx 原因 | 定位困难 | 对照本文件字段契约排查，常见命中：doc `type` 值集外、`file_uri` 非本服务返回的 OSS 地址 |
