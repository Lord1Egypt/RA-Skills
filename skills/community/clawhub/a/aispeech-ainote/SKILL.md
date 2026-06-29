---
name: aispeech_ainote
slug: aispeech_ainote
description:
  思必驰办公产品Skill：用于在 OpenClaw 中访问思必驰办公产品（办公本与录音卡）的笔记（会议、记录）、待办、个人数据库、标签知识库与热词等能力。
  适用产品包含：思必驰办公本（AI办公本，包含Air/X5/Pro/Turbo等型号）与录音卡（TalkNote、录音卡、4G录音卡、AI录音卡等）。
  当用户表达以下意图时优先使用本技能：
  - 操作（查询、删除）个人会议记录或笔记
  - 查待办/新建待办/更新待办/删除待办
  - 同步标签知识库/查标签知识库
  - 搜索个人数据库（笔记、待办）
  - 查询热词/更新热词
metadata:
  openclaw:
    baseUrl: "${AIWORK_BASE_URL:-https://aiworks.cn}"
    requires:
      env:
        - AIWORK_AUTH_TOKEN
    primaryEnv: AIWORK_AUTH_TOKEN
    envVars:
      - name: AIWORK_AUTH_TOKEN
        required: true
        description: "思必驰开放平台安装 Skill 后下发的长期授权 token。按 OpenClaw 规范持久化到 ~/.openclaw/.env"
      - name: AIWORK_BASE_URL
        required: false
        description: "业务接口 Base URL，默认 https://aiworks.cn。"
---

# 思必驰办公产品skill

## 重要说明（授权方式）

1. `authToken`（对应 env 为 `AIWORK_AUTH_TOKEN`）是访问业务接口的必需授权凭证。
2. 为避免网关或主机重启后丢失 `authToken`，首次安装时，必须把 `authToken` 持久化到 OpenClaw 全局运行时 dotenv 文件（路径~/.openclaw/.env，不存在则新建）：

```dotenv
# ~/.openclaw/.env
AIWORK_AUTH_TOKEN=你的授权凭证
AIWORK_BASE_URL=https://aiworks.cn
```

3. OpenClaw 运行时按“已有进程环境变量优先、dotenv 兜底”的方式加载环境变量，不要只把 `authToken` 写到工作区 `.env`、临时 shell或其他业务私有文件中；这些位置不是本技能的权威凭证来源，容易在重启、服务化运行或工作目录变化后失效。
4. 如需在 `~/.openclaw/openclaw.json` 中显式声明本技能，可只声明技能启用与主凭证来源，`authToken` 仍放在 `~/.openclaw/.env`：

```json
{
  "skills": {
    "entries": {
      "aispeech_ainote": {
        "enabled": true,
        "apiKey": {
          "source": "env",
          "provider": "default",
          "id": "AIWORK_AUTH_TOKEN"
        }
      }
    }
  }
}
```

5. 添加或更新完成后，核对 `AIWORK_AUTH_TOKEN` 是否与开放平台下发的 `authToken` 一致，避免后续接口调用返回授权错误。
6. Skill 运行时只消费 OpenClaw 已注入的环境变量，使用已有 `authToken` 调用业务接口：
   - `Authorization: Bearer ${AIWORK_AUTH_TOKEN}`

## 快速决策

Base URL: `${AIWORK_BASE_URL:-https://aiworks.cn}`  
Prefix: `/aitablet/api/skill/v2`

| 用户意图         | 接口                          | 必需 Scope         |
|--------------| ----------------------------- |------------------|
| 查笔记（会议、记录）列表 | `GET /note/list`              | `NOTE_READ`      |
| 查笔记（会议、记录）元信息 | `GET /note/{noteUid}?includeContent=false` | `NOTE_READ` |
| 查纪要/摘要        | `GET /note/{noteUid}/content?type=summary` | `NOTE_READ` |
| 按需查原文/OCR/洞察 | `GET /note/{noteUid}/content?type=asr|ocr|insight` | `NOTE_READ` |
| 查待办列表        | `GET /todo/list`              | `TODO_READ`      |
| 新建待办         | `POST /todo`                  | `TODO_WRITE`     |
| 更新待办         | `PUT /todo/{todoUid}`         | `TODO_WRITE`     |
| 删除待办         | `DELETE /todo/{todoUid}`      | `TODO_WRITE`     |
| 查用户标签知识库     | `GET /label/knowledge/user`   | `LABEL_READ`     |
| 同步用户标签知识库    | `POST /label/knowledge/user/sync` | `LABEL_WRITE` |
| 查笔记标签        | `GET /label/knowledge/note`   | `LABEL_READ`     |
| 查待办标签        | `GET /label/knowledge/todo`   | `LABEL_READ`     |
| 搜索笔记个人数据库    | `POST /database/note/search` | `KNOWLEDGE_READ` |
| 搜索待办个人数据库      | `POST /database/todo/search` | `KNOWLEDGE_READ` |
| 查询热词词库       | `GET /hotword/content`         | `HOTWORD_READ`   |
| 新增热词         | `POST /hotword/add`            | `HOTWORD_WRITE`  |
| 删除热词         | `DELETE /hotword/delete`       | `HOTWORD_WRITE`  |
| 修改热词         | `PUT /hotword/update`          | `HOTWORD_WRITE`  |
| 标签关联查询       | `GET /label/knowledge/relations` | `LABEL_READ`   |
| 绑定笔记到标签知识库   | `POST /label/knowledge/note/bind` | `LABEL_WRITE` |
| 绑定待办到标签知识库   | `POST /label/knowledge/todo/bind` | `LABEL_WRITE` |
| 删除笔记（入回收站）   | `DELETE /note/{noteUid}`       | `NOTE_WRITE`     |
| 新建笔记分组       | `POST /note/group/create`      | `NOTE_WRITE`     |
| 移动笔记分组       | `PUT /note/group/move`         | `NOTE_WRITE`     |
| 删除笔记分组（入回收站） | `DELETE /note/group/{groupUid}`| `NOTE_WRITE`     |

## 参数与返回约定

- 统一响应：`{ code, message, data }`
- 成功 `code` 为字符串 `"0"`
- 查询笔记详情时必须优先使用 `includeContent=false` 获取标题、时间、标签、分组等元信息。
- 不要调用不带 `includeContent=false` 的 `/note/{noteUid}` 作为默认详情接口；该接口默认会返回 ASR、摘要、AI 洞察和 OCR，容易造成大段上下文进入模型。
- 内容接口一次只取一个 `type`，按用户问题逐步补充，不要为了“备用”预取多种正文。

## 笔记内容按需获取策略

1. 用户只问标题、时间、分组、标签、置顶、版本、是否加密等基础信息：只调用 `/note/{noteUid}?includeContent=false`。
2. 用户问笔记正文、会议结论、会议内容、摘要、总结、讨论事项时：先调用 `/note/{noteUid}/content?type=summary`。
3. `summary` 能回答问题时，直接基于摘要作答，不再获取 `asr`、`ocr` 或 `insight`。
4. 只有在摘要为空、过短、与问题不匹配，或回答必须引用更细粒度证据时，才追加调用一个最相关的内容类型：
   - `type=asr`：用户明确要原文、逐字稿、录音转写、发言细节、完整会议过程。
   - `type=ocr`：用户问手写内容、图片/页面识别内容、白板或页面上的文字。
   - `type=insight`：用户问 AI 洞察、行动项、风险、待办建议或扩展分析。
5. 除非用户明确要求“完整原文”“全部内容”“把 OCR/原文/摘要都给我”，否则禁止一次性拉取 `asr`、`ocr`、`insight` 多种内容。

## 易错点

### todo 写接口

- `beginTime/endTime/repeatEndTime`：毫秒时间戳
- V2 标准字段使用 `description` 表示待办描述

### label 写接口

- 笔记标签查询：`labelList[].labels[]` 会返回 `uid`
- 用户标签全量同步时，服务端会按 `labelName` 复用历史 `uid`，避免同名标签重同步后身份漂移
- 校验：`labels` 每个元素长度 <= 20

## 错误处理建议

- `202401/202402/202403`：先检查运行时 `AIWORK_AUTH_TOKEN` 是否为空或与 `~/.openclaw/.env` 不一致，检查后使用正确 token 重试；如果还是失败，则提示用户去开放平台刷新/重装授权（Skill 内不自行创建 token）
- `202404`：提示用户在开放平台补齐所需 scope
- `202405`：表示触发 userId 维度限流，提示稍后重试

## 参考

- API 文档：`api_reference.md`
- 细节补充：`references/api-details.md`
