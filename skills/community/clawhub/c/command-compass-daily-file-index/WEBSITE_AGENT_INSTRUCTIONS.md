# 给官网 Agent 的开发调整指令

## 任务边界

你只负责官网 `www.wboke.com` 代码和数据结构调整，不修改 Windows 客户端代码，不修改本地技能包源码。

官网代码参考目录：

`D:\MyFiles\Work\javisHUD\备份-指令罗盘网站-20260622`

需要重点查看：

- `D:\MyFiles\Work\javisHUD\备份-指令罗盘网站-20260622\data\card-schema-v1.json`
- `D:\MyFiles\Work\javisHUD\备份-指令罗盘网站-20260622\data\command-vault.json`
- `D:\MyFiles\Work\javisHUD\备份-指令罗盘网站-20260622\api\_lib\store.js`
- `D:\MyFiles\Work\javisHUD\备份-指令罗盘网站-20260622\api\cards\search.js`
- `D:\MyFiles\Work\javisHUD\备份-指令罗盘网站-20260622\api\favorites.js`
- `D:\MyFiles\Work\javisHUD\备份-指令罗盘网站-20260622\RESOURCE_HOUND_INTEGRATION.md`
- `D:\MyFiles\Work\javisHUD\备份-指令罗盘网站-20260622\assets\wboke-site.js`

客户端实际兼容标准参考：

- `D:\MyFiles\Work\javisHUD\优化工作包-指令罗盘客户端-20260622\源码\docs\command-compass-integration-standard.md`
- `D:\MyFiles\Work\javisHUD\备份-指令罗盘技能包-20260622\技能源码\COMMAND_COMPASS_SKILL_ADAPTATION_REPORT.md`
- `D:\MyFiles\Work\javisHUD\备份-指令罗盘技能包-20260622\技能源码\examples\daily-file-index-cards.example.json`

## 总目标

让官网指令市场、收藏、资源猎犬、技能文件下载与 Windows 客户端的 CardSchema v1 完整对齐。

官网 API 返回的卡片必须能被 Windows 客户端直接映射为本地卡片：

- `instruction` 是唯一复制内容。
- `openTarget` 是统一打开地址。
- `resourceKind` 明确区分 `prompt`、`skill`、`workflow`、`template`、`file`、`folder`、`url`、`webFavorite`、`downloads`。
- 公开市场数据不得包含用户本地路径、Token、Cookie、密码、API Key。

## 一、更新 CardSchema v1

修改：

`D:\MyFiles\Work\javisHUD\备份-指令罗盘网站-20260622\data\card-schema-v1.json`

在保留现有必填公共字段的基础上，补充这些可选字段：

```json
{
  "libraryCategory": { "type": "string" },
  "libraryFolder": { "type": "string" },
  "openTarget": { "type": "string" },
  "localFilePath": { "type": "string" },
  "localFolderPath": { "type": "string" },
  "resourceUrl": { "type": "string" },
  "resourceKind": {
    "enum": ["prompt", "skill", "workflow", "template", "file", "folder", "url", "webFavorite", "downloads"]
  },
  "resourceMeta": { "type": "object", "additionalProperties": true },
  "iconId": { "type": "string" },
  "accent": { "type": "string" },
  "deep": { "type": "string" },
  "risk": { "enum": ["low", "medium", "high"] },
  "riskReasons": { "type": "array", "items": { "type": "string" } },
  "syncSource": { "type": "string" },
  "remoteId": { "type": "string" },
  "lastSyncedAt": { "type": "string" },
  "aiScore": { "type": "number" },
  "recommendationReason": { "type": "string" },
  "intentType": { "type": "string" },
  "xCommandCompass": { "type": "object", "additionalProperties": true }
}
```

`delivery.copyField` 必须保持 `instruction`。

## 二、更新官网卡片标准化逻辑

修改：

`D:\MyFiles\Work\javisHUD\备份-指令罗盘网站-20260622\api\_lib\store.js`

重点函数：

- `normalizeCardV1(item)`
- `searchCards(query)`

要求：

1. `prompt` 继续兼容，但导出必须标准化为 `instruction`。
2. 如果 `item.instruction` 存在，以 `instruction` 为准。
3. 如果只有 `prompt`，映射到 `instruction`。
4. 返回项必须补齐：
   - `schemaVersion: "1.0"`
   - `delivery.copyField: "instruction"`
   - `delivery.format: "text"`
   - `permissions` 六项布尔值
   - `resourceKind`
   - `xCommandCompass`
5. 官网市场普通提示词默认：
   - `resourceKind: "prompt"`
   - `openTarget: ""`
   - `libraryCategory` 可由 `category` 映射
   - `libraryFolder` 可由 `sub` 或 `marketSubCategory` 映射
6. 不要把 `job` 当成本地分类；`job` 只作为市场筛选维度。

## 三、更新指令市场搜索接口

修改：

`D:\MyFiles\Work\javisHUD\备份-指令罗盘网站-20260622\api\cards\search.js`

接口保持：

```http
GET /api/cards/search?q=&category=&sub=&job=&limit=
```

返回结构保持：

```json
{
  "ok": true,
  "categories": {},
  "items": [],
  "total": 0
}
```

但 `items` 内每张卡必须符合更新后的 CardSchema v1，并补充客户端兼容字段。

## 四、更新收藏接口

修改：

`D:\MyFiles\Work\javisHUD\备份-指令罗盘网站-20260622\api\favorites.js`

当前客户端已经使用：

- `GET /api/favorites`
- `POST /api/favorites`
- `DELETE /api/favorites`

要求：

1. 入参 `cardId` 必须是字符串，长度合理，过滤异常字符。
2. 返回 `favorites` 可以继续是 ID 数组。
3. 建议新增可选返回 `items`，内容为已收藏卡片的 CardSchema v1 完整对象，方便客户端后续一次性拉取收藏详情。
4. 无 Token 或错误 Token 返回：

```json
{ "ok": false, "error": "INVALID_TOKEN" }
```

5. 不要在响应里返回 Token 明文。

## 五、补齐资源猎犬正式 API

当前线上 `/api/hound` 和 `/api/hound/matches` 返回 404。请按以下接口实现：

### 获取状态

```http
GET /api/hound
Authorization: Bearer <deviceToken>
```

返回：

```json
{
  "ok": true,
  "enabled": true,
  "rules": [],
  "pendingCount": 0,
  "lastScanAt": ""
}
```

### 开关

```http
POST /api/hound
Content-Type: application/json
Authorization: Bearer <deviceToken>

{ "enabled": true }
```

### 保存规则

```http
POST /api/hound/rules
Content-Type: application/json
Authorization: Bearer <deviceToken>
```

规则字段：

```json
{
  "id": "rule_xxx",
  "name": "AI 编程工作流",
  "enabled": true,
  "keywords": ["Codex", "代码审查"],
  "categories": ["代码", "自动化"],
  "excludeKeywords": [],
  "minScore": 0.62,
  "notify": {
    "desktop": true,
    "inApp": true,
    "email": false
  },
  "syncMode": "confirm"
}
```

### 获取命中

```http
GET /api/hound/matches
Authorization: Bearer <deviceToken>
```

返回的 `items[].card` 必须符合 CardSchema v1，并设置：

```json
{
  "source": "hound",
  "syncSource": "wboke-hound",
  "resourceKind": "prompt",
  "xCommandCompass": {
    "syncMode": "confirm"
  }
}
```

### 收下

```http
POST /api/hound/matches/accept
Content-Type: application/json
Authorization: Bearer <deviceToken>

{
  "matchId": "match_001",
  "target": "favorites"
}
```

要求：

- 只在用户确认后写入收藏或个人库。
- 返回：

```json
{
  "ok": true,
  "synced": true,
  "cardId": "card_123"
}
```

### 忽略

```http
POST /api/hound/matches/reject
Content-Type: application/json
Authorization: Bearer <deviceToken>

{
  "matchId": "match_001",
  "reason": "not_relevant",
  "muteSimilar": false
}
```

## 六、数据存储建议

如果继续使用 Vercel KV，建议键名：

- `cc:hound:state:<email>`
- `cc:hound:rules:<email>`
- `cc:hound:matches:<email>`
- `cc:favorites:<email>`

规则与命中都必须按账号隔离。

不要存储用户本地路径、文件名、文件内容、电脑目录结构。

## 七、官网下载技能包

官网当前存在：

- `D:\MyFiles\Work\javisHUD\备份-指令罗盘网站-20260622\command-compass-skills.zip`

请用新版技能包替换网站下载文件。新版技能包由客户端 Agent 生成，来源目录：

`D:\MyFiles\Work\javisHUD\备份-指令罗盘技能包-20260622\发布包`

至少替换：

- `command-compass-skills.zip`

如果官网还有下载页缓存或静态引用，也要同步更新。

## 八、验收标准

1. `GET /api/cards/search?q=prompt` 返回 200，`items` 每项包含 `instruction`。
2. `items` 不再只依赖 `prompt`。
3. `delivery.copyField` 恒为 `instruction`。
4. `/api/hound` 不再 404。
5. `/api/hound/matches` 返回的卡片符合 CardSchema v1。
6. 无 Token 的账号、收藏、猎犬接口均返回标准 JSON 错误。
7. 公开市场数据不含用户本地路径。
8. 技能包下载文件可被 Windows 客户端导入。
