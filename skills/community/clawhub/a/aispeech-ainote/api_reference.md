# 思必驰办公产品skill OpenClaw Skill API 参考文档

## 1. 概述

### 1.1 接口基础信息

| 项目 | 说明                                                 |
|---|----------------------------------------------------|
| 协议 | HTTP/HTTPS                                         |
| 统一前缀 | `/aitablet/api/skill/v2`                           |
| 数据格式 | `application/json; charset=UTF-8`                  |
| 鉴权方式 | `Authorization: Bearer {AIWORK_AUTH_TOKEN}`（受保护接口） |

### 1.2 通用响应结构

```json
{
  "code": "0",
  "message": "success",
  "data": {}
}
```

- `code`：`"0"` 表示成功，其他为业务错误码。
- `message`：错误或成功消息。
- `data`：返回数据，可能是对象、数组或 `null`。

### 1.3 授权与 Scope

当前系统使用以下 Scope（大写）：

- `NOTE_READ`
- `TODO_READ`
- `TODO_WRITE`
- `LABEL_READ`
- `LABEL_WRITE`
- `KNOWLEDGE_READ`
- `HOTWORD_READ`
- `HOTWORD_WRITE`
- `NOTE_WRITE`

> 说明：本文件为 Skill 运行时接口文档，不包含开放平台侧的授权管理接口。
> `AIWORK_AUTH_TOKEN` 由开放平台在安装 Skill 时下发给 OpenClaw，用户可在安装时选择 scope，并支持永久授权。

---

## 2. 笔记接口

> 需要 Scope：`NOTE_READ`

### 2.1 查询笔记列表

- **GET** `/aitablet/api/skill/v2/note/list`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`

查询参数：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| pageNum | Integer | 否 | 默认 1 |
| pageSize | Integer | 否 | 默认 10，范围 1~100 |
| orderBy | String | 否 | `createTime` / `updateTime` |
| startTime | String | 否 | 格式 `yyyy-MM-dd HH:mm:ss` |
| endTime | String | 否 | 格式 `yyyy-MM-dd HH:mm:ss` |
| keyword | String | 否 | 标题关键字 |

### 2.2 查询笔记详情

- **GET** `/aitablet/api/skill/v2/note/{noteUid}`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`
- Query：
  - `includeContent`：可选，默认 `true`。OpenClaw 调用必须优先传 `false`，先获取轻量元信息，避免不必要的 OSS 内容读取和大段上下文注入。

返回核心字段（`SkillNoteVO`）：

- `noteUid`, `title`, `createTime`, `updateTime`, `labels[{name,uid,type}]`
- `labelNames`, `type`, `groupName`, `group{name,uid}`, `version`, `top`, `encryptType`
- `asrContent`, `summaryContent`, `insightContent`, `ocrContent`

按需策略：

- 用户只问标题、时间、分组、标签、置顶、版本等基础信息时，调用 `GET /note/{noteUid}?includeContent=false`。
- 用户问题需要笔记正文时，先调用 `GET /note/{noteUid}/content?type=summary` 获取纪要/摘要。
- `summary` 能回答问题时，不再获取其他正文。
- 当摘要为空、过短、没有覆盖用户问题，或回答必须引用更细粒度证据时，再调用一个最相关的 `GET /note/{noteUid}/content?type=asr|ocr|insight` 补充证据。
- 补充内容选择：原始会议细节用 `asr`；手写/页面信息用 `ocr`；AI洞察、行动项或扩展分析用 `insight`。
- 不要调用不带 `includeContent=false` 的详情接口作为默认路径，也不要默认全量拉取 `asr`、`ocr`、`insight`，除非用户明确要求完整原文或全量内容。

### 2.3 查询笔记指定内容

- **GET** `/aitablet/api/skill/v2/note/{noteUid}/content`
- Scope：`NOTE_READ`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`
- Query：`type=asr|summary|insight|ocr`

调用规则：

- 每次请求只返回一种内容，响应字段为 `data.content`。
- 先取 `type=summary`；只有摘要不足以回答时，按问题追加 `asr`、`ocr` 或 `insight` 中的一种。
- 不要为了备用同时请求多种正文内容。

返回字段（`SkillNoteContentVO`）：

- `noteUid`：笔记 UID
- `type`：内容类型
- `content`：指定类型内容

### 2.4 删除笔记（入回收站）

- **DELETE** `/aitablet/api/skill/v2/note/{noteUid}`
- Scope：`NOTE_WRITE`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`

---

## 3. 待办接口

### 3.1 查询待办列表

- **GET** `/aitablet/api/skill/v2/todo/list`
- Scope：`TODO_READ`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`

查询参数：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| status | Integer | 否 | `null`全部，`0`未完成，`1`已完成 |
| beginTime | Long | 否 | 开始时间（毫秒时间戳） |
| endTime | Long | 否 | 结束时间（毫秒时间戳） |
| pageNum | Integer | 否 | 页码 |
| pageSize | Integer | 否 | 每页大小 |


### 3.2 创建待办

- **POST** `/aitablet/api/skill/v2/todo`
- Scope：`TODO_WRITE`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`

请求体（`SkillTodoV2Form`）：

```json
{
  "todo": "完成周报",
  "beginTime": 1761922800000,
  "endTime": 1761926400000,
  "description": "可存放待办描述、会议链接等具体信息",
  "important": true,
  "done": false,
  "notifyAhead": "30m",
  "repeat": "weekly",
  "repeatEndTime": 1764601200000,
  "repeatCount": 10,
  "groupUid": "1000002643-DEFAULT"
}
```

字段说明：

- V2 标准字段为 `description`，语义是“待办描述”

字段校验：

- `notifyAhead` 最大长度 10
- `repeat` 最大长度 40
- `groupUid` 最大长度 45
- `todo`和`beginTime`均不能为空

### 3.3 更新待办

- **PUT** `/aitablet/api/skill/v2/todo/{todoUid}`
- Scope：`TODO_WRITE`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`
- 请求体同 `SkillTodoV2Form`

### 3.4 删除待办

- **DELETE** `/aitablet/api/skill/v2/todo/{todoUid}`
- Scope：`TODO_WRITE`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`

### 3.5 待办返回字段（`SkillTodoV2VO`）

时间字段已统一为毫秒时间戳：

- `beginTime`, `endTime`, `repeatEndTime`
- `syncTime`, `finishTime`, `createTime`, `updateTime`

其他字段：

- `uid`, `todo`, `description`, `important`, `done`, `notifyAhead`, `repeat`, `repeatCount`, `groupUid`

---

## 4. 标签接口

### 4.1 查询用户标签

- **GET** `/aitablet/api/skill/v2/label/knowledge/user`
- Scope：`LABEL_READ`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`

响应：

```json
{
  "code": "0",
  "message": "success",
  "data": {
    "labels": [
      {
        "uid": "label-uid-1",
        "name": "工作",
        "source": 0,
        "type": 2
      },
      {
        "uid": "label-uid-2",
        "name": "学习",
        "source": 0,
        "type": 2
      }
    ]
  }
}
```

### 4.2 同步用户标签

- **POST** `/aitablet/api/skill/v2/label/knowledge/user/sync`
- Scope：`LABEL_WRITE`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`

请求体：

```json
{
  "labels": [
    {
      "uid": "label-uid-2",
      "name": "学习",
      "source": 0,
      "type": 2
    }
  ]
}
```

校验规则：`labels` 中每个字符串长度不能超过 20。

兼容说明：

- 对象格式支持 `uid`、`name`、`source`、`type`
- 新增时uid可空，source=0即可，代表手动添加，1表示AI添加
- type 0=项目 1=客户 2=其他

### 4.3 查询笔记标签

- **GET** `/aitablet/api/skill/v2/label/knowledge/note`
- Scope：`LABEL_READ`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`
- 参数：`noteUids`（可多值）

返回的 `labelList[].labels[]` 中，标签对象包含：

- `uid`
- `name`
- `source`
- `type`

### 4.4 查询待办标签

- **GET** `/aitablet/api/skill/v2/label/knowledge/todo`
- Scope：`LABEL_READ`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`
- 参数：`todoUids`（可多值）

返回结构与笔记标签查询一致：`labelList[].noteUid` 字段承载待办 `uid`，`labels[]` 返回标签列表。

### 4.5 查询标签关联内容（笔记/待办）

- **GET** `/aitablet/api/skill/v2/label/knowledge/relations`
- Scope：`LABEL_READ`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`
- 参数：`uid` 或 `name`（二选一）

返回示例：

```json
{
  "code": "0",
  "message": "success",
  "data": {
    "labelUid": "label-uid-1",
    "labelName": "项目A",
    "notes": [{"uid":"note-1","title":"会议纪要","description":"描述内容","updateTime":"2026-05-05 12:00:00"}],
    "todos": [{"uid":"todo-1","todo":"跟进合同","done":false,"description":"待办描述","updateTime":"2026-05-05 12:00:00"}]
  }
}
```

### 4.6 标签知识库关联管理

- **POST** `/aitablet/api/skill/v2/label/knowledge/note/bind`
- **POST** `/aitablet/api/skill/v2/label/knowledge/todo/bind`
- Scope：`LABEL_WRITE`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`

请求体：

```json
{
  "labelUid": "label-uid-1",
  "targetUids": ["note-1","note-2"],
  "action": "add"
}
```

`action` 支持 `add/remove`，接口幂等。

---

## 5. 热词词库接口

### 5.1 查询热词词库

- **GET** `/aitablet/api/skill/v2/hotword/content`
- Scope：`HOTWORD_READ`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`

### 5.2 新增热词

- **POST** `/aitablet/api/skill/v2/hotword/add`
- Scope：`HOTWORD_WRITE`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`

请求体：

```json
{
  "word": "思必驰"
}
```

校验规则：`word` 长度为 2~10 个字符。

### 5.3 删除热词

- **DELETE** `/aitablet/api/skill/v2/hotword/delete`
- Scope：`HOTWORD_WRITE`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`

请求体：

```json
{
  "word": "思必驰"
}
```

### 5.4 修改热词

- **PUT** `/aitablet/api/skill/v2/hotword/update`
- Scope：`HOTWORD_WRITE`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`

请求体：

```json
{
  "oldWord": "思必驰",
  "newWord": "思必驰AI"
}
```

校验规则：`newWord` 长度为 2~10 个字符。

---

## 6. 笔记分组接口

### 6.1 新建分组

- **POST** `/aitablet/api/skill/v2/note/group/create`
- Scope：`NOTE_WRITE`
- 请求体中的 `version` 为可选，不传时服务端按当前版本处理。

### 6.2 移动分组

- **PUT** `/aitablet/api/skill/v2/note/group/move`
- Scope：`NOTE_WRITE`
- 规则：目标分组不能是当前分组或其子分组。

### 6.3 删除分组（入回收站）

- **DELETE** `/aitablet/api/skill/v2/note/group/{groupUid}`
- Scope：`NOTE_WRITE`
- 行为：分组及其子项进入回收站。

---

## 7. 知识库检索接口

> 需要 Scope：`KNOWLEDGE_READ`

### 5.1 搜索笔记知识库

- **POST** `/aitablet/api/skill/v2/database/note/search`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`

### 5.2 搜索待办知识库

- **POST** `/aitablet/api/skill/v2/database/todo/search`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`

请求体（`SkillKnowledgeSearchForm`）：

```json
{
  "query": "本周项目进度",
  "startTime": 1761609600000,
  "endTime": 1762214400000,
  "topN": 10
}
```

- `query` 必填，不能为空。
- `topN` 默认 10。

响应对象（`SkillKnowledgeVO`）：

- `uid`, `title`, `score`, `createTime`, `type`（`note` / `todo`）
- `contentFragments[]`：`content`, `score`, `fragmentType`

---

## 8. 错误码（关键）

### 6.1 授权相关（2024xx）

| code | message | 含义 |
|---|---|---|
| 202400 | 授权凭证为空 | 未提供 Authorization |
| 202401 | 授权凭证不存在 | token 不存在 |
| 202402 | 授权凭证已过期 | token 过期 |
| 202403 | 授权凭证已失效 | token 状态失效 |
| 202404 | 授权范围不足 | 缺少所需 scope |
| 202405 | Too many requests, please retry later | 触发 userId 维度限流 |

### 6.2 参数/业务相关（示例）

| code | message | 含义 |
|---|---|---|
| 201600 | 参数错误 | 通用参数校验失败 |
| 201602 | 待办不存在或无权限 | `todoUid` 不存在或无权访问 |
| 201613 | 内部服务异常 | 标签同步内部异常（如入库异常） |

---

## 9. 调用建议

1. Skill 运行时直接使用安装时下发的授权码，不在 Skill 内创建/删除授权。
2. 受保护接口统一携带 `Authorization: Bearer {AIWORK_AUTH_TOKEN}`。
3. 对 202401/202402/202403 提示用户在开放平台刷新或重装授权。
4. 对 202404 提示用户在开放平台补齐所需 scope。
5. 对 `todo` 与 `label` 写接口做好幂等重试与参数长度校验。
6. 对 `202405`，提示稍后重试，避免高频并发调用。


## 4. 调用建议

1. Skill 运行时仅使用安装时下发的 `AIWORK_AUTH_TOKEN`。  
2. 受保护接口统一携带 `Authorization: Bearer {AIWORK_AUTH_TOKEN}`。  
3. 对 `202401/202402/202403`，提示用户刷新/重装授权。  
4. 对 `202404`，提示用户补齐 scope。  
