# API Details

## 1) 通用响应

```json
{
  "code": "0",
  "message": "success",
  "data": {}
}
```

- 成功：`code == "0"`
- 失败：`code != "0"`

## 2) 授权说明（Skill 运行时）

- Skill 运行时只消费已有 `AIWORK_AUTH_TOKEN`。
- token 在安装 Skill 时由平台下发给 OpenClaw。

## 3) 关键错误码

| code | message | 说明 |
|---|---|---|
| 202400 | Authorization token is required | 未传 Authorization |
| 202401 | Authorization token is invalid | token 无效 |
| 202402 | Authorization token has expired | token 过期 |
| 202403 | Authorization token is disabled | token 失效 |
| 202404 | Authorization scope is insufficient | scope 不匹配 |
| 202405 | Too many requests, please retry later | 触发 userId 维度限流 |
| 201600 | 参数非法 | 请求参数不合法 |
| 201602 | 记录不存在 | todo 不存在或无权限 |
| 201613 | 内部服务异常 | 服务内部异常 |

## 4) Scope 速查

| Scope | 能力 |
|---|---|
| NOTE_READ | 读笔记 |
| NOTE_WRITE | 写笔记 |
| TODO_READ | 读待办 |
| TODO_WRITE | 写待办 |
| LABEL_READ | 读标签 |
| LABEL_WRITE | 写标签 |
| KNOWLEDGE_READ | 知识库检索 |

## 5) 时间字段规范

- Todo 相关时间统一为 Unix 毫秒时间戳（`Long`）。
- `beginTime/endTime/repeatEndTime/syncTime/finishTime/createTime/updateTime` 均为毫秒格式。
- Todo V2 接口统一使用 `description` 表示待办描述，可存储待办详情、会议链接等信息。
- Todo V2 请求仍兼容历史字段 `label`，但新接入方应优先使用 `description`。

## 6) 校验规则

- `SkillLabelForm.labels`：每个元素长度 <= 20
- `SkillTodoForm.notifyAhead`：长度 <= 10
- `SkillTodoForm.repeat`：长度 <= 40
- `SkillTodoForm.groupUid`：长度 <= 45

## 7) 标签同步兼容说明

- 用户标签 V2 查询返回 `uid`、`name`、`source`，便于调用方直接复用标签唯一标识。
- 用户标签 / 笔记标签 V2 同步同时兼容字符串数组与对象数组。
- 对象数组支持 `uid`、`name`、`source`；其中 `uid` 可用于显式传递标签唯一标识。
- 若不存在同名旧标签，则以 `labelName` 作为兜底标识生成逻辑。
- 笔记标签 V2 查询会返回标签 `uid`；若历史数据中缺失 `uid`，服务端会按同名用户标签尝试补全。

## 8) 产品适配与知识库口径

- 本技能名称：`思必驰办公产品skill`。
- 适用产品：
  - 思必驰办公本（思必驰AI办公本、AI办公本、办公本、办公本Air/X5/Pro/Turbo 等）
  - 录音卡（TalkNote、录音卡、4G录音卡、AI录音卡 等）
- 个人知识库：用户全量个人内容范围。
- 标签知识库：按标签 `uid` 圈定的内容子集，支持笔记与待办双维关联。

## 9) 笔记内容读取策略

- 默认详情读取：`GET /note/{noteUid}?includeContent=false`，只获取标题、时间、标签、分组等元信息。
- 默认正文读取：`GET /note/{noteUid}/content?type=summary`，先用纪要/摘要回答。
- 摘要不足时再追加一种内容：`asr` 用于原文/逐字稿/录音转写，`ocr` 用于手写或页面识别，`insight` 用于 AI 洞察、行动项和扩展分析。
- 不要默认调用 `includeContent=true` 的详情接口，也不要为了备用一次性获取 `asr`、`ocr`、`insight` 多种内容。
