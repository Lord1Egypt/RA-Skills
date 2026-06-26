# Agent 可直调飞书工具补丁（openclaw-lark）

> [!NOTE]
> 已提供英文版 Skill：`SKILL.en.md`（内容一致、语言为英语）。如需使用，可自行重命名为 `SKILL.md` 替换当前中文版本。

本文档是 `agent-feishu-direct-tools-patch` SKILL 的维护者说明版：在保留补丁动机与代码落点的基础上，补充 AI 执行规范、验收闭环、重启生效机制，以及在 Cursor / OpenClaw 对话中的使用方式。

适用扩展根目录：`extensions/openclaw-lark/`（若你 fork 或路径不同，请按相对结构对照）。

---

## 1. 背景与目标

典型业务场景是 **OpenClaw 多 Agent 协作**：用户在飞书聊天里给主 Agent 下达任务，主 Agent 再通过 `sessions_send` 在 OpenClaw 内部把工作派发给子 Agent（例如让子 Agent 创建日程）。

这类链路通常不会再次经过飞书入站，因此子 Agent 执行工具时拿不到完整、实时的飞书票据。若沿用默认兜底机制，工具调用可能回退到“主 Agent 所在应用身份”或默认账号语境，从而出现身份与权限错位：**真正执行任务的是子 Agent，但鉴权身份却落在主 Agent 对应 app 用户上**。

当主 Agent 恰好没有具体飞书工具权限（例如日历写权限），即使子 Agent 本身具备权限，也会报无权限错误；同时还会造成调用链路身份混乱、排障困难。

本补丁的目标是在 **Control UI / `sessions_send` / 非 webhook** 路径下，让 Agent 调用 `feishu_*` 工具时优先使用“当前执行 Agent 对应的应用用户身份”，确保：

- 选中正确 Feishu 子应用（`accountId`）；
- 当前用户 `open_id` 与该 app 语境一致；
- 避免日历 attendee 等接口的 cross-app `open_id` 错误；
- 解决多 Agent 派发下的“权限错位”与“调用链路身份混乱”问题。

核心链路：

`sessionKey -> accountId + senderOpenId -> synthetic ticket -> sync ALS -> ToolClient 与 getTicket 对齐`

---

## 2. 典型问题与根因

### 2.1 常见现象

- 飞书聊天中用户给主 Agent 下任务，主 Agent 通过 `sessions_send` 派发给子 Agent 执行；
- 子 Agent 实际在执行飞书工具，但鉴权身份回退到主 Agent 或默认账号；
- 结果是子 Agent 明明有权限，调用仍报“无权限 / scope 不足 / appId 不匹配”；
- 飞书私聊能成功，Control UI 调 `feishu_calendar_event` 失败；
- 错误提示落在错误 `appId`（经常误回退到 `main`）；
- 或出现 `open_id` 跨应用不一致。

### 2.2 根因拆解

1. `LarkTicket` 主要在 webhook 入站链路注入，Control UI 通常缺失。  
2. `createToolClient` 在无有效 ticket 时可能回退默认账号，或落入主 Agent 相关语境。  
3. OpenClaw 有 `sessionKey`（如 `agent:...:feishu:...:direct:ou_...`），但旧链路未完整传入工具栈，无法可靠恢复“当前执行 Agent 的 account + sender”。  
4. 即便生成 synthetic ticket，若不 `enterWith` 回 ALS，工具内 `getTicket()` 仍可能读到旧身份，导致 ToolClient 与工具体感知身份不一致。  

---

## 3. 方案总览（架构层）

| 层级 | 做什么 |
|------|--------|
| `index.js` | 在 `before_tool_call` / `after_tool_call` 绑定与清理 session 上下文；兼容 `(event, ctx)` / `(ctx, event)`；必要时从 `sessions.json` 反查 `sessionKey`。 |
| `agent-session-context.js` | ALS + `toolCallId -> sessionKey` Map + 短 TTL `lastSessionKey` 兜底。 |
| `session-key-feishu.js` | 解析 `feishu:direct` 与 `feishu:<accountId>:direct` 两种 sessionKey。 |
| `tool-client.js` | `createToolClient(config, accountIndex, toolCallId)`；sessionKey 合成身份优先于残留 ticket；并同步到 ALS。 |
| `lark-ticket.js` | 新增 `syncTicketContextForToolClient`，保证 `getTicket()` 与 ToolClient 一致。 |
| `helpers.js` + OAPI/MCP | `toolClient(toolCallId)` 全量透传 `toolCallId`。 |
| `calendar/event.js` | `effectiveSenderOpenId` 采用 `getTicket()?.senderOpenId ?? sessionBoundSenderOpenId`。 |
| `auth-errors.js` | `AppScopeMissingError` 增加 `appId=`，便于多账号排障。 |

---

## 4. 关键改动清单（与 SKILL 同步）

以下改动与 `agent-feishu-direct-tools-patch/SKILL.md` 保持一致：

- 新增 `src/core/agent-session-context.js`  
  - 提供 `bindToolCallContext`、`registerSessionKeyForToolCall`、`resolveAgentSessionKeyForToolCall` 等。
- 新增 `src/core/session-key-feishu.js`  
  - 提供 `parseFeishuDirectSessionIdentity`、`resolveFeishuAccountIdForAgent`。
- 修改 `src/core/lark-ticket.js` 与 `src/core/lark-ticket.d.ts`  
  - 新增 `syncTicketContextForToolClient(ticket)`。
- 修改 `src/core/tool-client.js` 与 `src/core/tool-client.d.ts`  
  - `createToolClient(config, accountIndex = 0, toolCallId)` 三参化。  
  - sessionKey 身份优先，生成 synthetic ticket 后同步 ALS。
- 修改 `src/tools/helpers.js` 与 `src/tools/helpers.d.ts`  
  - `toolClient: (toolCallId) => createToolClient(config, accountIndex, toolCallId)`。
- 修改根 `index.js`  
  - 兼容双参 hook；写入/清理 session context；支持 `sessions.json` 反查。
- 修改 `src/core/auth-errors.js`  
  - `AppScopeMissingError` 消息附带 `appId`。
- 修改 `src/tools/oapi/calendar/event.js`  
  - 全部分支统一 `effectiveSenderOpenId` 优先级。
- 全量工具 callsite 对齐  
  - `execute(_toolCallId, params)` + `toolClient(_toolCallId)`；含 OAPI 与 `src/tools/mcp/shared.js`。

---

## 5. 与 SKILL 一致的执行规范（新增）

> 本节来自 SKILL 的新增约束，建议在文档评审和二次移植时按此执行。

### 5.1 执行前必须确认

- 在任何源码改动前，先向操作者说明：  
  - 将进行哪些文件修改；  
  - 风险与回滚方式；  
  - 改完必须重启 Gateway。  
- 获得明确“同意执行”后再改代码。

### 5.2 执行顺序与闭环

- 按章节逐条实施（不要跳节，不要只改局部）；  
- 每节至少做“结构校验 + 语义校验”；  
- 有一项失败就继续修复，不以“部分通过”收官；  
- 收官时输出改动文件、改动类别、未完成项（若有）。

### 5.3 强制重启提醒

- 补丁是磁盘改动，运行态模块不会自动热替换；  
- 必须重启 OpenClaw Gateway（或加载该插件的 Node 进程）后再验证。  

### 5.4 失败兜底

- 先按回滚清单恢复；  
- 若仍异常且用户接受覆盖本地修改，可重装官方插件基线：  
  - `npx -y @larksuite/openclaw-lark install`  

---

## 6. sessionKey 与配置约定

- sessionKey 形态：
  - `agent:<agentId>:feishu:direct:ou_<32hex>`
  - `agent:<agentId>:feishu:<accountId>:direct:ou_<32hex>`
- `openclaw.json` / 等价配置中的 `bindings`：
  - `bindings[].match.channel === "feishu"`
  - `bindings[].match.accountId` 映射到 `channels.feishu.accounts.<accountId>`
- 多账号场景需确保每个 app 的授权与 scope 对应正确用户；错误时可依据 `appId=` 快速定位。

---

## 7. 在 Cursor 等 AI 开发工具中如何使用 SKILL（新增）

推荐用途：**一次性补丁执行**、合并冲突后重打补丁、版本升级后二次移植核对。

### 7.1 推荐流程

1. 在对话中明确指令：按 `agent-feishu-direct-tools-patch/SKILL.md` 执行补丁。  
2. 要求 Agent 先给“执行前说明”，你确认后再动代码。  
3. Agent 按章节完成修改并给出文件清单。  
4. 你重启 Gateway。  
5. 按本文第 9 节做 DM + Control UI 冒烟验证。  

### 7.2 最佳实践

- 作为临时任务技能使用，不建议长期常驻“默认技能集”；  
- 每次补丁前先做 Git 提交/分支或目录备份；  
- 升级 `openclaw-lark` 后，先对照关键签名再复用补丁（尤其 hook 形态、`createToolClient`、`execute` 签名）。

---

## 8. 直接在 OpenClaw 聊天中如何使用（新增）

当你希望“运行时 Agent”也能读到这个 SKILL，可短期采用以下方式：

1. 把 `agent-feishu-direct-tools-patch/` 放到 `skills.load.extraDirs` 可扫描目录下（推荐复制，便于后删）。  
2. 在对话里明确触发：  
   - “按 `agent-feishu-direct-tools-patch` 给 `openclaw-lark` 打补丁。”  
3. 也可以直接把技能压缩包发给 OpenClaw 机器人（在飞书聊天中发送），机器人会自动读取并执行其中的流程说明。  
4. 执行完成后，从技能目录移除该临时副本或禁用条目。  
5. 重启 Gateway，避免补丁技能长期干扰日常对话。  

说明：把 SKILL 暴露给对话 Agent 只是“给它看说明”，**不能替代源码修改和重启**。

---

## 9. 部署与验证

1. 保存全部源码改动。  
2. 重启 Gateway / 托管 OpenClaw 的 Node 进程。  
3. 在 Control UI（同 Agent、同会话语境）测试日历创建等写操作。  
4. 观察日志：  
   - `createToolClient: synthetic Lark identity from sessionKey`  
   - 如发生覆盖：`sessionKey overrides LarkTicket`  
5. 如工具支持 `_debug`，核对 `ticket_account_id`、`ticket_sender_open_id`、`user_open_id` 一致性。  

---

## 10. 回滚与故障排查

### 10.1 回滚建议

- 建议事先备份以下关键文件：  
  `src/core/lark-ticket.js`、`src/core/lark-ticket.d.ts`、`src/core/tool-client.js`、`src/core/tool-client.d.ts`、`index.js`、`src/tools/helpers.js`、`src/tools/helpers.d.ts`、`src/tools/oapi/calendar/event.js`，以及新增的两个核心文件。  
- 回滚要成套恢复，避免“半补丁状态”。

### 10.2 故障排查清单

| 症状 | 检查项 |
|------|--------|
| 仍落到 `main` 的 `appId` | `before_tool_call` 是否拿到 `sessionKey`；`parseFeishuDirectSessionIdentity` 是否命中；`bindings` 映射是否正确。 |
| cross-app / open_id 不一致 | 是否调用 `syncTicketContextForToolClient`；工具是否仍读旧缓存身份。 |
| hook 不生效 | 插件是否注册 `before_tool_call`；参数顺序兼容是否正确。 |
| `sessions.json` 反查失败 | 当前实现依赖 `parsed.sessions[]` 的 `sessionId/key`；若是旧格式需扩展解析或确保网关传 `ctx.sessionKey`。 |

---

## 11. 与 SKILL 文档分工

- `SKILL.md`：给 Agent 的“执行手册”（怎么改、按什么顺序、如何验收）。  
- 本文档：给人类维护者/评审者的“设计与运维说明”（为什么改、改在哪里、如何上线和回滚）。  
- 已提供英文版 Skill：`SKILL.en.md`（内容一致、语言为英语）；如需使用，可自行重命名为 `SKILL.md` 替换当前中文版本。  

两者配合使用：**Agent 按 SKILL 执行，维护者按本文复核。**

---

*文档内容以仓库当前实装为准；跨分支移植时请用 `git diff` 核对文件路径与函数签名。*

