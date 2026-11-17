# transweb.cn 通用 AI Skill 接口参考

本文件记录 `transweb-ai` 使用/运行应用与 PPT 的接口。创建 Agent/Skill 应用的接口见 `transweb-create/references/api.md`。实现来源：

- `interface/test.js`：`getLoginedData`、`queryQuestionData`、`setDocumentStatus`、`getUserData`
- `interface/gpt.js`：`aiGatewayRequest`、`_aiRequestConfirm`、`recordRequestItem`
- `interface/apiKey.js`：`createApiKey`
- `custom/RestFulConfig.js`：`requiredScope`

## 鉴权

```http
Authorization: Bearer ak_live_...
Content-Type: application/json
```

API Key 由 transweb.cn 账号创建，服务端只存哈希。Scope 白名单：

```text
account:read  account:write  doc:read  doc:write  ai:chat  points:read  points:transfer
```

| scope | 本 skill 用途 |
| --- | --- |
| `doc:read` | `list` → `/user/getLoginedData`（必需） |
| `ai:chat` | `run` → `/gpt/aiGatewayRequest`（必需） |
| `account:read` | 可选，`whoami` / 读取积分 |

### Key profile

配置文件支持多套 Key：

```json
{
  "active": "work",
  "profiles": {
    "default": {"apiKey": "ak_live_...", "baseUrl": "https://transweb.cn"},
    "work": {"apiKey": "ak_live_...", "baseUrl": "https://transweb.cn"}
  }
}
```

- `config use <name>` 切换 `active`。
- `configure --profile <name> --api-key <key>` 新建/更新并激活。
- 单次命令 `--profile <name>` 只对该次生效；`TRANSWEB_PROFILE` 可指定默认 profile。
- 旧的扁平 `{apiKey, baseUrl}` 会按 `default` profile 读取；`configure`/`config use` 会写成 profiles 结构到当前解析到的配置路径（`--config` / `TRANSWEB_CONFIG` / 项目或用户级默认路径）。

缺少 scope：

```json
{"ret":3,"message":"无权限（缺少 scope）。"}
```

## 1. 列出账号下的应用

```http
POST /user/getLoginedData
```

需要 `doc:read`。它查询 `pptItem` 集合，并按当前会话 `folderName` 隔离。

请求：

```json
{
  "table": "pptItem",
  "pageSize": 100,
  "pageNo": 1,
  "condition": {"publishStatus": "true"}
}
```

- `publishStatus: "true"`：只取已发布、可用的应用；不传则包含未发布（可能上千条）。
- 服务端默认排除 `_delete: true`。
- 支持 `lastTime` keyset 分页，但本 skill 用 `pageNo`/`isEnd` 翻页。

响应（注意是 `code`，不是 `ret`）：

```json
{
  "code": 0,
  "message": "success",
  "pagination": {"total": 45, "pageNo": 1, "pageSize": 100},
  "mode": "skip",
  "isEnd": true,
  "data": [
    {
      "_id": "...",
      "documentId": "76f7de9504bad022a8978e9fe084df0f",
      "title": "演示文稿",
      "name": "演示文稿",
      "description": "...",
      "introduce": "...",
      "type": "创意写作类",
      "tags": "[\"数据分析、幻灯片\"]",
      "category": "未定义",
      "appLabel": "创智通",
      "publishStatus": "true",
      "folderName": "1714628260"
    }
  ]
}
```

**应用 ID = `data[].documentId`**，32 位十六进制。`title`/`name` 是展示名，`description`/`introduce` 是用途说明，`tags` 可能是 JSON 字符串。

翻页：读取 `pagination.total`、`isEnd`；`pageSize` 最大 100。

## 2. 公开市场应用（自建无匹配时回退）

```http
GET /user/getPublishedList?pageSize=100&pageNo=1&sort=-1
```

该接口没有标注 `requiredScope`，API Key 可直接调用。它查询所有用户的 `pptItem`，默认条件 `publishStatus: "true"`、排除 `_delete: true`，按 `publishTime` 倒序。

响应（注意是 `ret`，不是 `code`）：

```json
{
  "ret": 0,
  "total": 65,
  "pageSize": 100,
  "current": 1,
  "isEnd": true,
  "data": [
    {
      "documentId": "76f7de9504bad022a8978e9fe084df0f",
      "title": "演示文稿",
      "name": "演示文稿",
      "description": "...",
      "introduce": "...",
      "type": "创意写作类",
      "tags": "["数据分析、幻灯片"]",
      "category": "未定义",
      "appLabel": "创智通",
      "appOwner": "创博",
      "creator": "刘文津",
      "folderName": "1714628260",
      "publishStatus": "true",
      "usageCount": 242,
      "publishTime": 1781786006425
    }
  ]
}
```

- 应用 ID 同样是 `documentId`。
- 有些公开应用只有 `documentId`，没有 `title`/`description`（历史数据），这类不适合语义选择。
- 市场里也可能包含自己的应用；`--source both` 会按 ID 去重，自建优先。

### 来源优先级

`list --source`：

| 值 | 行为 |
| --- | --- |
| `auto`（默认） | 先 `getLoginedData`；`--query` 过滤后没有匹配，再 `getPublishedList` |
| `mine` | 只 `getLoginedData` |
| `published` | 只 `getPublishedList` |
| `both` | 两者都取，自建优先去重 |

返回字段：

- `selectedSource`：`mine` / `published` / `both`
- `fallback`：`true` 表示自建无匹配、已回退公开市场
- `ownTotal` / `publishedTotal`
- `apps[].source`：每个应用的来源

`run` 对两种来源的 ID 一视同仁：生成、存档、权限、链接流程完全相同。

## 3. 执行一个应用

```http
POST /gpt/aiGatewayRequest
```

需要 `ai:chat`。

请求：

```json
{
  "documentId": "<应用 ID>",
  "context": "用户需求 / 上一步输出",
  "apiName": "深度求索",
  "model": "deepseek-v4-flash"
}
```

- 服务端按 `documentId` 从 `pptItem` 读取该应用的 prompt、`apiName`、`model`。
- `apiName` / `model` 可省略，省略时用应用自身配置。
- `context` 作为 user message；应用 prompt 作为 system message。
- 生成消耗积分，按 token 计费。

响应（内容在 `usage.result`）：

```json
{
  "ret": 0,
  "usage": {
    "result": "模型原始输出（可能是 JSON、文本、代码等）",
    "pointsCost": 250,
    "prompt_tokens": 2793,
    "completion_tokens": 7522
  }
}
```

错误：`ret:1` 登录/Key 无效；`ret:2` 积分不足；`ret:3` 缺 scope。

## 4. 找到服务端的存档

`aiGatewayRequest` 返回后，服务端由 `recordRequestItem` 异步写入 `questionData`：

```json
{
  "_id": "...",          // 链接里的 dataId
  "documentId": "<应用 ID>",
  "folderName": "...",
  "result": "模型原始输出",
  "data": "通常同 result",
  "versionId": "mmh3.x64.hash128(JSON.stringify(extractJSON(result)))",
  "_time": 1794387674000
}
```

去重规则：`versionId + folderName + documentId`。相同内容重复生成不会新增记录。

查询：

```http
GET /user/queryQuestionData?table=questionData&condition=...&sort=...&pageNo=1&pageSize=50
```

本 skill 的条件：

```json
{
  "documentId": "<应用 ID>",
  "folderName": {"$in": ["1714628260", 1714628260]}
}
```

排序 `{"_time":-1}`。服务端还会按 `isShare === "true" || folderName === 会话 folderName` 过滤。

匹配：用本次 `usage.result` 与每行 `result`/`data` 比较：

1. 原始字符串完全相等
2. 压缩 JSON 完全相等
3. 空白归一化后相等（纯文本）
4. 解析为 JSON 对象后深度相等

这样兼容代码围栏、前后说明文字、压缩/格式化差异和旧版本去重。

## 5. 设置访问权限

```http
POST /user/setDocumentStatus
```

把存档 `isShare` 设为 `"true"`：

```json
{
  "table": "questionData",
  "cKey": "_id",
  "_id": "<dataId>",
  "key": "isShare",
  "value": "true"
}
```

成功：

```json
{"ret":0,"result":{"n":1,"nModified":1,"ok":1},"data":{"isShare":"true"},"message":"操作成功。"}
```

没有标注 `requiredScope`，但要求会话有 `folderName`；非管理员只能更新自己 `folderName` 下的记录。

设置后 skill 会**不带 Key** 再查一次 `_id`，确认匿名可访问；成功则 `accessible: true`。

## 6. 链接格式

```text
{baseUrl}/?solo=true&dataView=true&dataId={存档 _id}&id={应用 ID}
```

- `id`：`pptItem.documentId`（应用 ID）。
- `dataId`：`questionData._id`（存档版本）。
- `solo=true`：只渲染应用。
- `dataView=true`：只读查看。

单例直接返回该链接；链式返回每一步的链接，最后一步是 `link` / 最终结果。

## 7. 链式执行

`run --ids id1,id2,...` 按顺序执行。每步：

```text
context = 上一步 usage.result   （--chain-mode result，默认）
        | 原始需求              （requirement）
        | 原始需求 + 上一步结果 （both）
```

每步独立查询存档、设置权限、生成链接。某步失败时停止，已完成的 `steps` 保留在输出的 `completed` 里。

注意：不同应用的输入/输出 schema 不统一；下游应用若要求特定 JSON，可能需要在 `--input` 或上游结果上做适配。可以先单例跑一次确认输出。

## 8. PPT 专用入口（原 transweb-ppt 已并入）

做 PPT/幻灯片/演示文稿的需求不再单独走一个技能，而是由 `transweb-ai` 的 `ppt` 命令固定调用官方应用：

```text
documentId = 76f7de9504bad022a8978e9fe084df0f
```

执行链路与普通应用完全相同：

```text
POST /gpt/aiGatewayRequest {documentId: PPT_APP_ID, context: 大纲/需求}
→ 返回 usage.result（Reveal.js JSON）
→ GET /user/queryQuestionData 匹配存档
→ POST /user/setDocumentStatus {table:"questionData", cKey:"_id", key:"isShare", value:"true"}
→ 链接 ?solo=true&dataView=true&dataId=<_id>&id=76f7...
```

`ppt` 命令额外解析 `usage.result` 里的 `title` 和 `slides`，输出：

```json
{
  "ok": true,
  "link": "...",
  "dataId": "...",
  "documentId": "76f7de9504bad022a8978e9fe084df0f",
  "title": "演示文稿标题",
  "slides": 12,
  "pointsCost": 250,
  "archived": true,
  "accessible": true,
  "elapsedMs": 113000
}
```

如果 `usage.result` 不是 JSON，或缺少非空 `slides`，`ppt` 会报 `invalid_output`；不会把无效内容当 PPT 存档。`transweb-ai` 不读取其他技能的 Key，必须显式配置自己的 API Key。

## 9. documentType：agent / skill

`run` 执行前调用：

```http
GET /user/getDocumentData?table=pptItem&key=documentId&documentId=<id>
```

取 `data[0].documentType`：

| 值 | `run` 输出 |
| --- | --- |
| `"agent"` | 字符串结果 `usage.result`；不查存档、不生成链接 |
| `"skill"` | 归档后返回 `?solo=true&dataView=true&dataId=...` 链接 |
| 缺失/未知 | 按 skill 兼容 |

`list --with-document-type` 会逐个补查该字段。

## 错误速查

| 返回 | 含义 | 处理 |
| --- | --- | --- |
| `code:1` / `ret:1 未登录` | Key 无效/过期/撤销 | 重建 Key |
| `ret:3` / `code:3` | 缺 `doc:read` 或 `ai:chat` | 重建 Key 并勾选 |
| `ret:2 积分余额不足` | 积分不足 | 充值/减少链式步数 |
| `HTTP 404` | 路径/域名错误 | 用 `https://transweb.cn` |
| 查询结果为空 | 存档未写入/计费失败 | `--wait 30`，确认积分 |
| `accessible:false` | 权限更新失败/非所有者 | 查看 `accessError` |
