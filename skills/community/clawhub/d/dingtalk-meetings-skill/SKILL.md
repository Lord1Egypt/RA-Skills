---
name: dingtalk-meetings-skill
description: 当用户想要操作钉钉日历/会议时使用本 Skill。支持：创建日程/会议、修改日程、删除/取消日程、查询日程列表与详情、添加/移除参会人、查询参会人列表、查询空闲/忙碌时段、预定会议室、查询空闲会议室、推荐会议时间、响应日程邀请、管理日历权限。当用户想操作飞书、Google Calendar、Outlook 等其他平台日历，只操作本地日历文件，管理钉钉文档/IM 消息/群组时，不要使用本 Skill。
license: MIT
compatibility: Requires dingtalk-calendar MCP server (StreamableHttp transport, mcpId=1050). Optionally uses dingtalk-contacts MCP server (mcpId=2400) for user lookup. Compatible with any MCP-capable agent (Claude Code, Cursor, VS Code, Roo Code, Gemini CLI, Codex, etc.). Auto-detects Claude Code; falls back to writing config files or manual setup for other agents.
---

# 钉钉会议日程

通过钉钉日历官方 MCP Server 全面管理会议与日程。

## 语言规则

**始终使用用户输入的语言进行回复。** 如果用户用英文提问，则全程用英文回复；如果用户用中文，则全程用中文回复。无法判断时默认使用中文。

## 欢迎提示（首次交互或用户询问能力时展示）

当用户首次触发本 Skill 或主动询问"你能做什么"时，展示以下引导信息：

```
我可以帮你管理钉钉日历和会议，具体能力包括：

📅 日程管理
  • 创建/修改/删除日程会议
  • 添加/移除参会人
  • 响应日程邀请（接受/拒绝/暂定）

🔍 查询
  • 查看日程列表与详情
  • 查询空闲/忙碌时段
  • 智能推荐会议时间

🏢 会议室
  • 查询空闲会议室并预定
  • 管理会议室分组

📋 其他
  • 管理日历本与共享权限
  • 添加日程附件

💡 使用示例：
  "帮我创建明天下午2点的周会，拉上张三李四"
  "查看我今天的日程安排"
  "取消下午的产品评审会"
  "帮我看看明天下午哪些会议室是空的"

⚠️ 说明：
  • 查询日程、删除日程、查看空闲时段等操作只需日历 MCP
  • 如果创建日程需要拉其他同事参加，还需配置通讯录 MCP（按姓名查找 userId）
  • 只创建自己的日程（不拉人）则不需要通讯录 MCP
```

根据用户语言调整展示内容。非首次交互时不重复展示，除非用户主动询问。

## 能力范围

**日程管理**
- 创建日程（标题、时间、地点、参与人、描述、提醒、循环规则等）
- 修改日程信息（标题、时间、地点、描述等）
- 删除/取消日程
- 响应日程邀请（接受/拒绝/暂定）

**查询**
- 列出指定时间范围内的日程
- 查看日程详情（标题、时间、地点、参与人、描述、会议室等）
- 查询用户空闲/忙碌时段
- 推荐会议时间（基于参会人空闲情况）

**参会人管理**
- 添加/移除日程参与人
- 查看日程参与人列表及响应状态

**会议室管理**
- 查询空闲会议室
- 为日程预定会议室
- 移除日程中的会议室
- 查询会议室分组和标签

**日历本管理**
- 列出/搜索日历本
- 查看日历本信息
- 管理日历共享权限（添加/删除/查看 ACL）

**附件**
- 为日程添加附件（需先上传到钉盘获取 fileId）

**不负责：**
- 飞书、Google Calendar、Outlook 等其他平台
- 只操作本地日历文件（无云端操作）
- 钉钉 IM 消息、文档操作、企业成员管理（查人请用钉钉通讯录 MCP）

## 前置条件

### 必须：日历 MCP

钉钉日历 MCP Server 必须已配置到当前 Agent 的 MCP 设置中，服务名称为 `dingtalk-calendar`。

如果日历 MCP 工具不可用，先走**初始化流程**，再执行任何操作。

### 按需：通讯录 MCP

钉钉通讯录 MCP Server（服务名 `dingtalk-contacts`，mcpId=2400）**仅在以下场景需要**：

| 场景 | 是否需要通讯录 MCP | 原因 |
|------|------------------|------|
| 创建日程并拉其他人参加 | **需要** | 需要通过姓名/手机号查找参会人 userId |
| 创建仅自己的日程 | 不需要 | 不涉及其他人 |
| 查询/列出日程 | 不需要 | 只读操作 |
| 删除日程 | 不需要 | 只需 eventId |
| 修改日程时间/标题/地点 | 不需要 | 只需 eventId |
| 添加参会人到已有日程 | **需要** | 需要查找参会人 userId |
| 移除参会人 | 不需要 | 可从日程详情获取已有参会人 userId |
| 查询空闲/忙碌 | 不需要 | 使用 userId 查询，如已知则不需查找 |
| 预定会议室 | 不需要 | 不涉及人员查找 |

**判断规则**：当用户要创建或修改日程且涉及"拉其他人"时，检查通讯录 MCP 是否可用。如不可用，告知用户：
> 创建包含其他参会人的日程需要通讯录 MCP 来查找同事的 userId。你可以：
> 1. 配置通讯录 MCP（推荐，后续可按姓名查找同事）
> 2. 直接提供参会人的 userId（如果你已知的话）
> 3. 先创建只有自己的日程，稍后再添加参会人

## 初始化流程（首次使用或 MCP 不可用时）

1. 告知用户访问帮助手册页面并完成开通：
   > 请打开以下链接，使用钉钉账号登录后，点击页面上的【开通服务】按钮：
   > https://aihub.dingtalk.com/#/detail?mcpId=1050&detailType=marketMcpDetail

2. 开通后复制页面右侧 **StreamableHttp URL**（不是 JSON Config）

3. 请用户将 URL 粘贴给你

4. 收到 URL 后，按以下顺序尝试注册 MCP 服务（`dingtalk-calendar` 为服务名，必须为 ASCII）。

   如果用户还需要通讯录 MCP（用于按姓名查找参会人 userId），同样流程为 `dingtalk-contacts` 注册（mcpId=2400 的 URL）。

   **方案 A — Claude Code**（优先尝试，运行命令看是否成功）：
   ```bash
   claude mcp add --transport http --scope user dingtalk-calendar "<用户提供的 URL>"
   ```
   成功则跳到步骤 5。

   **方案 B — 写入配置文件**（通用方案，大多数 Agent 均可用）：

   检测当前环境存在哪些配置文件，找到第一个匹配项写入：

   | Agent | 配置文件（全局） | 配置文件（项目级） | `mcpServers` 键名 |
   |-------|---------------|----------------|-----------------|
   | Cursor | `~/.cursor/mcp.json` | `.cursor/mcp.json` | `mcpServers` |
   | VS Code Copilot | `~/Library/Application Support/Code/User/mcp.json`（Mac）<br>`%APPDATA%\Code\User\mcp.json`（Win） | `.vscode/mcp.json` | `servers` |
   | Roo Code | — | `.roo/mcp.json` | `mcpServers` |
   | Gemini CLI | `~/.gemini/settings.json` | — | `mcpServers` |
   | OpenAI Codex | `~/.codex/config.json` | — | `mcpServers` |

   向目标文件追加（若文件已有 `mcpServers`/`servers`，只添加新条目，不覆盖原有内容）：

   ```json
   {
     "mcpServers": {
       "dingtalk-calendar": {
         "type": "http",
         "url": "<用户提供的 URL>"
       }
     }
   }
   ```
   > VS Code Copilot 的 `.vscode/mcp.json` 使用 `"servers"` 而非 `"mcpServers"`，写入时注意区分。

   成功写入则跳到步骤 5。

   **方案 C — 手动兜底**（方案 A/B 均不适用时）：

   向用户展示以下信息，请其参照所用 Agent 的文档手动添加 MCP 服务，完成后回来继续：
   ```
   传输类型：StreamableHttp（HTTP）
   服务名称：dingtalk-calendar
   URL：<用户提供的 URL>
   ```
   用户手动配置完成后，本 Skill 只需确认 MCP 工具可用即可继续。

   > URL 中含有个人 API Key，写入配置后不要在回复中重复显示完整 URL。

5. MCP 配置写入后，提示用户重启 Agent 客户端以使 MCP 生效，重启后回来继续操作即可。

### 安全规则

- MCP 服务 URL 含有个人 API Key，**不得出现在任何版本控制文件中**；写入配置后不要在回复中重复显示完整 URL
- 如果用户将 URL 粘贴到聊天中，立即写入配置后不再引用

## 默认路径

1. 确认日历 MCP 工具可用（若不可用，进入初始化流程）
2. 理解用户意图，映射到对应 MCP 工具（见工具映射表）
3. 如需要 eventId 但用户未提供：调用 `list_calendar_events` 列出近期日程，让用户确认后再操作
4. 如需添加参会人但用户只提供了姓名/手机号：
   - 先检查 `references/contacts.cache` 是否有缓存的 userId（见参会人缓存机制）
   - 缓存未命中时，通过通讯录 MCP 的 `search_user_by_key_word` 或 `search_user_by_mobile` 查找 userId
   - 查到后写入缓存供下次使用
5. 创建日程时：为所有未指定的参数填充推荐值（见参数推荐值表）
6. **执行前确认**（只读操作除外）：向用户展示**完整日程详情**，收到明确同意后再调用 MCP 工具
7. 执行操作
8. 报告结果：操作类型、日程标题、日程时间（如有）

### 创建日程参数推荐值

创建日程时，用户未明确指定的参数应按以下规则填充推荐值：

| 参数 | 推荐值规则 | 示例 |
|------|----------|------|
| `summary` | 根据上下文推断 | "项目周会"、"需求评审" |
| `startDateTime` | 用户提到的时间，未提则取明天 14:00 | `2026-06-12T14:00:00+08:00` |
| `endDateTime` | 默认开始时间 +1 小时 | `2026-06-12T15:00:00+08:00` |
| `timeZone` | `Asia/Shanghai` | — |
| `freeBusy` | `busy` | — |
| `location` | 空（不填） | — |
| `description` | 空（不填），用户提及时才填 | — |
| `calendarId` | `primary` | — |
| `recurrence` | 不填（非循环日程） | — |

> **注意**：推荐值必须填入后在确认摘要中完整展示给用户，用户可修改任何字段。

### 执行前确认规则

**需要确认的操作**（所有会写入或修改云端数据的操作）：
`create_calendar_event`、`update_calendar_event`、`delete_calendar_event`、`add_calendar_participant`、`remove_calendar_participant`、`add_meeting_room`、`delete_meeting_room`、`add_acl`、`delete_acl`、`add_attachments`、`respond`

**无需确认的操作**（只读）：
`list_calendar_events`、`get_calendar_detail`、`get_calendar_participants`、`query_busy_status`、`list_suggested_event_times`、`query_available_meeting_room`、`list_calendars`、`get_calendar`、`search_calendar`、`list_acls`、`list_meeting_room_groups`、`list_org_room_labels`

**确认摘要格式 — 创建日程（必须展示完整详情）：**

```
即将创建以下日程，请确认：

标题：<summary>
时间：<startDateTime> ~ <endDateTime>
时区：<timeZone>
忙碌状态：<freeBusy>
地点：<location，未填则显示"无">
描述：<description，未填则显示"无">
参与人：<参会人姓名列表，或"仅自己">
会议室：<roomIds，未填则显示"无">
循环：<recurrence，未填则显示"不循环">

如需修改任何字段，请直接告诉我要改什么。
确认请回复「是」或「确认」，取消请回复「否」或「取消」。
```

**确认摘要格式 — 其他操作：**

```
即将执行以下操作，请确认：

操作：<修改 / 取消 / 邀请参会人 / 移除参会人 / 预定会议室 / 移除会议室>
日程：<日程标题>
时间：<开始时间> ~ <结束时间>（如有）
变更详情：<具体修改内容或操作说明>

确认请回复「是」或「确认」，取消请回复「否」或「取消」。
```

收到取消时：停止操作，不重试，告知用户已取消。

## MCP 工具映射

详见 `references/mcp-tools.md`。常用映射如下：

| 用户意图 | MCP 工具 |
|---------|---------|
| 创建日程/会议 | `create_calendar_event` |
| 修改日程信息 | `update_calendar_event` |
| 删除/取消日程 | `delete_calendar_event` |
| 查看近期日程列表 | `list_calendar_events` |
| 查看日程详情 | `get_calendar_detail` |
| 查看日程参与人 | `get_calendar_participants` |
| 添加参会人 | `add_calendar_participant` |
| 移除参会人 | `remove_calendar_participant` |
| 响应日程（接受/拒绝/暂定） | `respond` |
| 查询空闲/忙碌时段 | `query_busy_status` |
| 推荐会议时间 | `list_suggested_event_times` |
| 查询空闲会议室 | `query_available_meeting_room` |
| 预定会议室 | `add_meeting_room` |
| 移除会议室 | `delete_meeting_room` |
| 添加日程附件 | `add_attachments` |
| 管理日历共享权限 | `add_acl` / `delete_acl` / `list_acls` |
| 列出/搜索日历本 | `list_calendars` / `search_calendar` |
| 按姓名查找参会人 userId | 通讯录 MCP：`search_user_by_key_word` |
| 按手机号查找参会人 userId | 通讯录 MCP：`search_user_by_mobile` |

## 失败处理

- **MCP 工具不可用**：停止，进入初始化流程，不要猜测或尝试其他方式调用
- **未提供目标日程**：先用 `list_calendar_events` 列出近期日程，让用户确认后再操作
- **参会人查找失败**：当通过姓名或手机号无法找到用户时，告知用户并请其确认参会人的准确信息。可使用通讯录 MCP 的 `search_user_by_key_word`（按姓名）或 `search_user_by_mobile`（按手机号）辅助查找 userId
- **时间冲突**：创建日程前可用 `query_busy_status` 检查参会人是否空闲，如有冲突展示给用户。也可直接用 `list_suggested_event_times` 推荐空闲时段
- **会议室不可用**：用 `query_available_meeting_room` 查询空闲会议室，展示可用选项给用户选择
- **API 报错（权限/鉴权类）**：当 API 返回权限不足、无权限、鉴权失败、Forbidden、Unauthorized 等错误时，除了展示原文错误信息外，提示用户可能尚未开通所在组织的钉钉开发者权限，引导用户参考以下链接完成开通：
  > 请访问钉钉开发者入门文档，确认你已在所在组织中开通了开发者权限：
  > https://open.dingtalk.com/document/dingstart/dingtalk-developer
  >
  > 开通步骤简述：登录钉钉开放平台 → 选择对应组织 → 完成开发者认证/开通。完成后重新尝试操作。
- **其他 API 报错**：原文展示错误信息，不猜测原因，不自动重试

## 关键约束

- `delete_calendar_event`：组织者删除将通知所有参与者，参与者删除仅从自己日历移除。执行前**必须**明确告知用户，获得确认后再执行
- 时间格式：`create_calendar_event` 和 `update_calendar_event` 使用 ISO-8601 格式（如 `2026-06-11T14:00:00+08:00`）
- `list_calendar_events` 使用**毫秒级时间戳**（如 `1718100000000`），注意与 ISO-8601 区分
- `query_busy_status` 和 `query_available_meeting_room` 也使用**毫秒级时间戳**
- 创建日程时如用户未指定时区，默认使用 `Asia/Shanghai`（UTC+8）
- 创建日程时如用户未指定时长，默认 1 小时
- 日程参与人最多 500 人，支持 userId 或 openDingTalkId
- 每个日程最多预定 5 个会议室
- 修改日程参与人需使用 `add_calendar_participant` / `remove_calendar_participant`，不能用 `update_calendar_event`
- `add_attachments` 需要先将文件上传到钉盘获取 fileId
- 操作完成后，从返回值中提取关键信息（日程标题、时间、参与人数等）简明展示给用户

## 参会人缓存机制

为了减少重复查询，通过通讯录 MCP 查到的 userId 会缓存到 `references/contacts.cache` 文件中。

### 缓存文件格式

`references/contacts.cache` 为 JSON 格式，已被 `.gitignore` 排除，不会进入版本控制：

```json
{
  "contacts": {
    "张三": { "userId": "user123", "name": "张三", "updatedAt": "2026-06-11T10:00:00+08:00" },
    "李四": { "userId": "user456", "name": "李四", "updatedAt": "2026-06-11T10:00:00+08:00" }
  }
}
```

### 读取顺序

当需要查找参会人 userId 时：

1. 先读取 `references/contacts.cache`，按姓名或手机号模糊匹配
2. 缓存命中 → 直接使用缓存的 userId，不再调用通讯录 MCP
3. 缓存未命中 → 调用通讯录 MCP 查询，查到后写入缓存
4. 缓存文件不存在或为空 → 直接调用通讯录 MCP 查询

### 缓存更新规则

- 每次通过通讯录 MCP 成功查到 userId 后，立即写入缓存
- 如果 API 返回 userId 无效（人已离职等），从缓存中删除该条目
- 缓存文件不存在时，首次写入会自动创建

### 用户主动管理缓存

- 用户可以说"记住张三是 user123"，直接写入缓存
- 用户可以说"删除缓存中的李四"，从缓存中移除
- 用户可以说"显示已缓存的联系人"，展示缓存内容

## 资源导航

- `references/mcp-tools.md` — 全部 MCP 工具详细说明，按场景分组
- `references/contacts.cache` — 参会人 userId 缓存（自动维护，不入版本控制）
