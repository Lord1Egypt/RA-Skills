---
name: aispeech_ainote
slug: aitablet
description:
  思必驰办公产品skill：用于在 OpenClaw 中访问思必驰办公产品（办公本与录音卡）的笔记（会议、记录）、待办、个人数据库、标签知识库与热词等能力。
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
      env: ["AIWORK_AUTH_TOKEN"]
    optionalEnv: ["AIWORK_BASE_URL"]
    tokenManagement:
      source: "思必驰开放平台应用管理"
      lifecycle: "长期有效，无过期时间。安装时配置，平台需持久化存储"
      problem: "安装后首次执行有效，但平台重启/环境重置后 AIWORK_AUTH_TOKEN 丢失（仅配置在 ~/.aispeech/aitablet.json 时），导致后续调用返回 202401"
      requirement: "平台必须通过 OpenClaw 配置 skills.entries.<slug>.env.AIWORK_AUTH_TOKEN 持久化 token，确保重启后环境变量不丢失"
      configLocations:
        - path: "skills.entries.<slug>.env.AIWORK_AUTH_TOKEN"
          description: "推荐方式。OpenClaw 运行时自动注入到 skill 环境变量，重启后不丢失"
        - path: "env.vars.AIWORK_AUTH_TOKEN"
          description: "备选方式。注入到网关进程全局环境变量，所有 skill 可见"
        - path: "~/.aispeech/aitablet.json"
          description: "文件存储。agent 需手动读取并导出为环境变量，重启后不会自动加载"
      failureDetection:
        - code: 202401
          description: "授权凭证无效（token 为空或错误）"
        - code: 202402
          description: "授权已过期"
        - code: 202403
          description: "授权被撤销"
      autoRecovery:
        description: "检测到授权失效时，优先检查 AIWORK_AUTH_TOKEN 环境变量是否为空（常见原因）"
        steps:
          - step: 1
            action: "检测到 202401/202402/202403 错误码"
          - step: 2
            action: "检查 $AIWORK_AUTH_TOKEN 环境变量是否为空"
          - step: 3
            action: "如果为空，尝试从 ~/.aispeech/aitablet.json 读取 token 并导出到环境变量"
          - step: 4
            action: "重试请求，确认 token 是否真的失效"
---

# 思必驰办公产品skill

## 重要说明（授权方式）

1. `authToken`（对应 env 为 `AIWORK_AUTH_TOKEN`）是访问业务接口的必需授权凭证。
2. 首次安装时，**必须持久化存储 token**，否则重启后会丢失。提供三种配置方式：

### 方式一（推荐）：OpenClaw 配置注入

在 OpenClaw 配置文件（`openclaw.json`）中添加：

```json
{
  "skills": {
    "entries": {
      "aitablet": {
        "env": {
          "AIWORK_AUTH_TOKEN": "你的授权凭证"
        }
      }
    }
  }
}
```

OpenClaw 运行时在加载此 skill 时自动将 `AIWORK_AUTH_TOKEN` 注入到环境变量，重启后不丢失。**这是最可靠的配置方式。**

### 方式二（备选）：网关全局环境变量

```json
{
  "env": {
    "vars": {
      "AIWORK_AUTH_TOKEN": "你的授权凭证"
    }
  }
}
```

### 方式三（文件备份）：本地配置文件

```json
// ~/.aispeech/aitablet.json
{
  "aitablet-skill": {
    "env": {
      "AIWORK_AUTH_TOKEN": "你的授权凭证",
      "AIWORK_BASE_URL": "https://aiworks.cn"
    }
  }
}
```

> ⚠️ 仅用此方式时，重启后 `$AIWORK_AUTH_TOKEN` 不会自动加载到环境变量。
> agent 需要在运行时手动执行 `export AIWORK_AUTH_TOKEN=$(cat ~/.aispeech/aitablet.json | jq -r '.[].env.AIWORK_AUTH_TOKEN')`。
> 建议配合方式一或方式二一起使用，作为兜底备份。


添加完成后，重点核对下`authToken`是否与所给的一致，避免后续无法调用接口

3. Skill 运行时，需要读取配置文件中的env变量设置到当前环境变量，使用已有 `authToken` 调用业务接口：
   - `Authorization: Bearer ${AIWORK_AUTH_TOKEN}`

## 快速决策

Base URL: `${AIWORK_BASE_URL:-https://aiworks.cn}`  
Prefix: `/aitablet/api/skill/v2`

| 用户意图         | 接口                          | 必需 Scope         |
|--------------| ----------------------------- |------------------|
| 查笔记（会议、记录）列表 | `GET /note/list`              | `NOTE_READ`      |
| 查笔记（会议、记录）详情 | `GET /note/{noteUid}`         | `NOTE_READ`      |
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

## 易错点

### todo 写接口

- `beginTime/endTime/repeatEndTime`：毫秒时间戳
- V2 标准字段使用 `description` 表示待办描述

### label 写接口

- 笔记标签查询：`labelList[].labels[]` 会返回 `uid`
- 用户标签全量同步时，服务端会按 `labelName` 复用历史 `uid`，避免同名标签重同步后身份漂移
- 校验：`labels` 每个元素长度 <= 20

## 错误处理建议

- `202401/202402/202403`：提示用户去开放平台刷新/重装授权（Skill 内不自行创建 token）
- `202404`：提示用户在开放平台补齐所需 scope
- `202405`：表示触发 userId 维度限流，提示稍后重试

## 参考

- API 文档：`api_reference.md`
- 细节补充：`references/api-details.md`
