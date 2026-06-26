---
name: agent-feishu-direct-tools-patch
description: >-
  One-time/on-demand patch for openclaw-lark (no webhook LarkTicket paths). Implements
  agent-session-context, session-key-feishu, syncTicketContextForToolClient, createToolClient
  third arg, hooks, calendar effectiveSenderOpenId, toolClient sweep. After file edits,
  tell the user what changed and that they MUST restart the Gateway. BEFORE starting file edits,
  Agent must brief the user and wait for explicit confirmation. On failure or Feishu broken after
  patch, user may reinstall with: npx -y @larksuite/openclaw-lark install. Prefer AI-assisted dev
  tools or temporary OpenClaw skill load—avoid keeping this skill permanently enabled in
  skills.entries. Use when porting or re-applying after merge conflicts.
---

# openclaw-lark：Agent 无飞书票据直调工具（完整补丁 Skill）

**执行约定**：以下路径相对于 **`openclaw-lark` 扩展根目录**（含 `index.js`、`src/` 的目录）。实施 Agent **须先完成「执行前：向用户说明并待确认」** 并得到用户 **明确同意** 后，再按 **§B–§M** 顺序修改代码，并跑文末 **验收命令**，即与下列已验证实现 **语义等效**。  
**强制要求**：不得以“当前版本结构不同/未搜到同名片段”为由直接跳过任一章节；必须在当前代码中找到语义等价位置完成改动（见 **§0.3 严格执行与闭环验收协议**）。

- 在飞书插件 **2026.3.18**、**2026.3.25** 对应代码结构上测试可用。
- **升级风险**：飞书官方若后续改动插件目录、`before_tool_call` 形态、`execute` 签名或核心模块名，本节中的路径/补丁点可能失效；升级后须逐项对照并重新冒烟（Control UI + 飞书 DM）。

**不要**与本 Skill 之外的其它 Skill 混读；本文自成闭环。

---

## 执行前：向用户说明并待确认（Agent 第一优先级，先于 §B–§M）

**在创建/修改任何源码文件（从 §B 起）之前**，实施 Agent **必须先**向用户发一条 **补丁前说明**（当前对话渠道：飞书、Control UI、IDE 侧等均可），让用户知情并 **明确确认** 后再继续。不得在用户仅浏览、提问或未表态的情况下擅自改代码。

### 说明里应包含的要点（Agent 按需组织成自然语言）

1. **做什么**：本 Skill 会按章节 **批量修改 `openclaw-lark` 扩展**（新建 2 个文件、改核心模块与大量工具文件），用于解决「无飞书 webhook 票据时 Agent 直调飞书工具」的身份与账号问题（概要见 **§A**）。
2. **使用方式**：按 **§B–§M** 顺序执行；改完后用户需 **自行重启 OpenClaw Gateway** 才生效（见 **「补丁与 OpenClaw 运行态」**）；验证见 **§O**。
3. **风险**：环境与官方版本差异可能导致合并冲突或补丁点不匹配；飞书插件升级后需重新对照 Skill **§ 开头的版本说明**。
4. **建议**：动手前 **备份** `openclaw.json` 中 `plugins.installs.openclaw-lark.installPath` 所指目录，或使用 **git** 提交/分支，便于回滚。
5. **失败或补丁后飞书仍不可用**：可先按 **§P** **回滚** 手工改动；若仍异常、希望恢复 **官方可安装基线**，在用户 **知情并接受可能被覆盖的本地修改** 的前提下，可执行官方安装命令重装飞书插件（需本机 Node / npx 可用）：

```bash
npx -y @larksuite/openclaw-lark install
```

重装会按 **@larksuite/openclaw-lark** 发布的流程处理扩展，**可能覆盖你对该插件目录的手写修改**；执行前请用户自行确认。重装后仍须按 OpenClaw 文档 **启用插件并重启 Gateway**。

6. **一次性 Skill**：若将本 Skill 挂进 OpenClaw 技能列表，建议 **短期使用**，见 **§0.2**。

### 何时可以开始改代码

- **必须**：用户用明确措辞表示 **同意执行本补丁**（例如「确认执行」「开始打补丁」「同意，请按 Skill 修改」等；随 locale 理解同义表达）。
- **禁止**：用户仅说「讲讲 Skill」「什么是补丁」而未确认执行 → **只解释，不改文件**。
- 用户确认后，**再**从 **§B** 起执行；执行全过程仍须遵守 **§0** 的收官汇报与 **§「补丁与 OpenClaw 运行态」** 的重启说明。

---

## 0. 执行收尾与用户告知（实施 Agent 必做）

本节适用于 **各类 AI 辅助开发工具中的 Agent**（如 Cursor、GitHub Copilot、Codeium、Windsurf 等）、**OpenClaw 对话里的 Agent**，以及 **任何按本 Skill 执行补丁的实施 Agent**。在 **§B–§M 的代码改动全部完成**（含 §M 的 `rg` 验收，若环境可运行）之后，**必须**向用户发出 **一条清晰的收官消息**（飞书回复、Control UI 回复、或当前会话通道均可），内容至少包括：

1. **结果状态**：成功完成 / 部分完成（并说明卡在哪一步）/ 未改文件（仅咨询）。
2. **改动了哪些文件**：逐项列出路径（相对于 **`openclaw-lark` 扩展根目录**），并标明 **新建** 或 **修改**，例如：
   - 新建：`src/core/agent-session-context.js`、`src/core/session-key-feishu.js`
   - 修改：`src/core/lark-ticket.js`、`src/core/lark-ticket.d.ts`、`src/core/tool-client.js`、`src/core/tool-client.d.ts`、`src/tools/helpers.js`、`src/tools/helpers.d.ts`、`index.js`、`src/core/auth-errors.js`、`src/tools/oapi/calendar/event.js`，以及 §M 列出的各 `toolClient(_toolCallId)` 工具文件（若你还改了超出清单的文件，一并列出）。
3. **做了哪些类别的调整**（给用户看的短摘要，无需贴大段代码），例如：新增会话上下文与 sessionKey 解析、合成 Lark ticket 并同步 ALS、`createToolClient` 增加 `toolCallId`、插件 hook 绑定 sessionKey、日历身份优先 `getTicket()`、权限错误带 `appId`、全量工具传入 `toolCallId` 等。
4. **网关重启提醒（强制）**：说明 **磁盘上的修改在重启 OpenClaw Gateway（或加载该插件的 Node 进程）之前不会生效**；请用户 **自行按环境重启**（实施 Agent 若无明确授权与能力，**不要声称已替用户重启**）。
5. **可选后续**：提醒用户重启后可按 **§O** 做飞书 DM + Control UI 冒烟；若曾临时把本 Skill 挂进 OpenClaw 技能目录，可按 **§0.2** 拆除以免常驻。
6. **若执行失败或补丁后飞书仍异常**：提醒用户可先 **§P 回滚**；仍不可用则可在接受「官方重装可能覆盖本地修改」的前提下执行  
   `npx -y @larksuite/openclaw-lark install`（与 **「执行前：向用户说明并待确认」** 一致），重装后重启 Gateway。

---

## 0.2 一次性补丁：如何避免「常态化待在」OpenClaw 技能列表

本 Skill 是 **按需执行的一次性工程补丁**，不是日常对话要常驻引用的业务技能。建议按下面方式使用，避免它 **长期出现在待选技能里**、干扰其它 Agent：

| 做法 | 说明 |
|------|------|
| **只用本地 AI 工具、不挂 OpenClaw** | 把 `agent-feishu-direct-tools-patch` 放在所用工具支持的 **skills / 规则 / 上下文** 目录，或在对话里 **@ / 粘贴 `SKILL.md` 路径** 执行；**不要**写入 `openclaw.json` 的 `skills`。这样 OpenClaw Gateway 运行时 **完全看不到** 本 Skill。 |
| **临时挂到 OpenClaw** | 若必须让 **Gateway 里的 Agent** 读本文：可 **短期** 将本目录 **复制** 到已有 `skills.load.extraDirs` 下的某个文件夹，**用完即删该副本**（或移除 `extraDirs` 里为补丁专加的目录），并 **重启 Gateway**。列表里不再出现即恢复常态。 |
| **勿长期 `enabled: true`** | 若配置里有 `skills.entries.<name>`：对本 Skill **不要**设为长期启用；需要打补丁时再打开（若你的 OpenClaw 版本支持按条目开关），打完改回 **禁用** 或删掉对应条目。 |
| **不要依赖「Agent 自动选技能」** | 由用户 **明确一句话触发**（例如：「按 openclaw-lark 的 agent-feishu-direct-tools-patch 打补丁」），避免把补丁 Skill 与日常 `team-agent-onboarding` 类技能混在同一常驻集合里。 |
| **随仓库或压缩包分发** | 将整个 `agent-feishu-direct-tools-patch` 目录纳入 Git 或打包发给别人即可复用；**是否**让运行时装载，与 **是否在磁盘保留** 是两回事——保留文件 ≠ 必须加入 `skills.entries` 长期启用。 |

**与 §「让 OpenClaw 里的对话 Agent 也能加载本 Skill」的关系**：那几条是「**短期需要时**怎么挂载」；默认仍推荐 **在 AI 辅助开发工具里执行 + 用完不挂 Gateway**，或 **临时挂载 → 打完补丁即拆**。

---

## 0.3 严格执行与闭环验收协议（实施 Agent 必须遵守）

本节用于避免“执行了但漏改/误改/跳过”。实施 Agent 在用户确认执行后，必须按以下闭环进行，直到全部通过：

1. **逐条施工**：按 **§B→§M** 顺序执行；每节完成后立即自检，不得一次性粗放改完再回头补。
2. **禁止跳节**：任何一节（含 **§L**）都不可因“版本差异”直接标记不适用；若代码结构不同，必须在当前实现中定位语义等价位置并完成同等改动。
3. **双重校验**：每节至少做  
   - **文本/结构校验**（关键符号、函数签名、调用形态、导出项）；  
   - **行为意图校验**（是否满足该节目标语义，而非仅字符串出现）。
4. **失败即继续修复**：只要有任一校验不通过，必须继续修改并重验；禁止在“部分通过”状态下收官。
5. **收官门槛（全部同时满足）**：  
   - §B–§M 每一节均通过；  
   - §M 的 `toolClient()` 无参调用检查通过（非注释/文档语境）；  
   - 对关键高风险点做定向复核：`index.js` hook 参数兼容、`createToolClient(config, accountIndex, toolCallId)` 三参链路、`calendar/event.js` 的 `effectiveSenderOpenId` 优先顺序。
6. **证据化汇报**：收官消息必须带“章节验收清单”，至少列出 §B–§M 每节“已通过”的一句证据（例如命中函数名/签名/调用形态），而非只说“已完成”。
7. **未全绿不得结束**：若工具环境限制导致某条无法验证，状态必须标为“未完成/待验证”，并继续处理可处理项；禁止宣称“补丁完成”。

---

## 补丁与 OpenClaw 运行态（AI 辅助工具与网关通用，必读）

### 为什么必须重启网关（或等价进程）

- OpenClaw 在 **启动 Gateway 时** 把插件（含 `openclaw-lark`）**加载进 Node 进程**；改磁盘上的 `.js` **不会**自动热替换已加载模块。
- **仅保存文件 ≠ 线上生效**。改完 §B–§M 后，必须 **重启加载该插件的进程**，补丁才会在 **飞书 / Control UI / sessions_send** 里体现。

### 建议操作顺序（实施者照做）

1. **确认改的是运行时要用的目录**：`openclaw.json` → `plugins.installs.openclaw-lark.installPath`（或你本机实际启用的扩展目录）应与正在编辑的 **`openclaw-lark` 根目录** 一致；若从不一致的副本改代码，重启后仍会用旧代码。
2. **保存全部相关文件**（含新建的两个 `src/core/*.js`）。
3. **重启 OpenClaw Gateway**（或任何托管 `openclaw`、负责加载插件的 Node 进程）：
   - **前台运行**：在运行 Gateway 的终端里停止进程（如 Ctrl+C），再按你平时的方式重新启动（例如 `openclaw gateway` 或项目文档中的启动命令）。
   - **守护进程 / systemd / Docker / 远程机器上的 Gateway**：在 **实际跑 Gateway 的那台机器** 上对 **同一服务** 执行重启（与官方「改插件配置后重启 Gateway」一致）。
4. **再跑 §O 的验证**（飞书 DM + Control UI 各测一次）。

### 在 AI 辅助开发工具里用本 Skill

- 由 Agent 或人工按 §B–§M 改代码 → **必须执行上面第 3 步（重启 Gateway）** → 再验证。  
- 若跳过重启，会误以为「补丁无效」。

### 让 OpenClaw 里的对话 Agent 也能「加载」本 Skill（可选、建议短期）

本仓库里 Skill 目录名为 `agent-feishu-direct-tools-patch/`（内含 `SKILL.md`）。OpenClaw 默认 **不会**自动扫描飞书扩展内部子目录；若 **临时** 要在 **运行时 Agent** 侧可读，任选其一：

1. **复制**（优先于软链，便于打完补丁整目录删除）整个 `agent-feishu-direct-tools-patch` 到 **`openclaw.json` 里 `skills.load.extraDirs` 已列出的目录**之一，使存在 `.../agent-feishu-direct-tools-patch/SKILL.md`。打完补丁后 **删除该副本** 并重启 Gateway，见 **§0.2**。
2. 或在 `skills.load.extraDirs` 中 **短期增加** 一条指向「仅含本 Skill 父目录」的路径；**用完从配置中移除** 后重启 Gateway。
3. 若使用 `skills.entries`：**不要**长期把本 Skill 对应条目设为 `enabled: true`；需要执行补丁时再打开，执行完改回禁用（行为因 OpenClaw 版本而异，以文档为准）。

说明：**插件代码补丁**与 **把 SKILL 给运行时读** 是两件事——前者改 `openclaw-lark` 源码并重启即生效；后者只是把 **操作说明** 暴露给 Agent，**不能替代**源码修改与重启。**默认推荐在本机 AI 辅助开发工具中执行本 Skill**，避免补丁文档常驻 Gateway 技能列表（**§0.2**）。

---

## A. 要解决的问题

| 类型 | 说明 |
|------|------|
| 入口 | Control UI、sessions_send 等 **无 webhook**，无完整 `LarkTicket`。 |
| 账号 | `createToolClient` 回退到默认账号 → **误用 main** 等，报错里 **appId 不对**。 |
| 身份 | OpenClaw 已有 `sessionKey`（`agent:…:feishu:…:direct:ou_…`），未进工具栈 → 无法选 account + senderOpenId。 |
| ALS 不一致 | 合成 ticket 后未写回 ALS → `getTicket()` 仍陈旧 → **open_id 跨应用**（日历参会人等）。 |
| Hook 边界 | `toolCallId` 缺失或 `(event,ctx)` 顺序不同、`await` 丢 ALS → 需 **Map + 短 TTL lastSessionKey**。 |

**目标行为**：`sessionKey → 解析 accountId/senderOpenId → 合成 ticket（且优先于残留 LarkTicket）→ syncTicketContextForToolClient → ToolClient 与 getTicket 一致 → 所有工具 `toolClient(toolCallId)`。**

---

## B. 新建文件 1：`src/core/agent-session-context.js`

完整落盘为以下文件（逐字一致）：

```javascript
"use strict";
/**
 * Propagate OpenClaw agent sessionKey into the Feishu tool stack without a Feishu webhook.
 *
 * `before_tool_call` receives ctx.sessionKey; we store it in AsyncLocalStorage and by
 * toolCallId so createToolClient() can synthesize Lark identity for Control UI / sessions_send.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.bindToolCallContext = bindToolCallContext;
exports.bindAgentSessionKeyForToolCall = bindAgentSessionKeyForToolCall;
exports.getToolCallContext = getToolCallContext;
exports.getAgentSessionKey = getAgentSessionKey;
exports.resolveAgentSessionKeyForToolCall = resolveAgentSessionKeyForToolCall;
exports.registerSessionKeyForToolCall = registerSessionKeyForToolCall;
exports.clearSessionKeyForToolCall = clearSessionKeyForToolCall;
const node_async_hooks_1 = require("node:async_hooks");
const store = new node_async_hooks_1.AsyncLocalStorage();
/** Fallback when ALS does not propagate into tool execute (await boundaries). */
const sessionKeyByToolCallId = new Map();
/** Last-bound sessionKey (short TTL) when both ALS and Map miss. */
let lastSessionKey = "";
let lastSessionKeyAt = 0;
const LAST_SESSION_KEY_TTL_MS = 5000;
const MAX_TOOL_CALL_SESSION_KEYS = 512;
function bindToolCallContext(params) {
    const sessionKey = typeof params?.sessionKey === "string" ? params.sessionKey.trim() : "";
    const agentId = typeof params?.agentId === "string" ? params.agentId.trim() : "";
    if (!sessionKey && !agentId) {
        return;
    }
    if (sessionKey) {
        lastSessionKey = sessionKey;
        lastSessionKeyAt = Date.now();
    }
    store.enterWith({
        ...(sessionKey ? { sessionKey } : {}),
        ...(agentId ? { agentId } : {}),
    });
}
function bindAgentSessionKeyForToolCall(sessionKey) {
    bindToolCallContext({ sessionKey });
}
function getToolCallContext() {
    return store.getStore();
}
function getAgentSessionKey() {
    return store.getStore()?.sessionKey;
}
/**
 * Prefer ALS; else sessionKey registered for this toolCallId in before_tool_call.
 */
function resolveAgentSessionKeyForToolCall(toolCallId) {
    const fromAls = store.getStore()?.sessionKey;
    if (fromAls) {
        return fromAls;
    }
    if (toolCallId && typeof toolCallId === "string") {
        const fromMap = sessionKeyByToolCallId.get(toolCallId);
        if (fromMap) {
            return fromMap;
        }
    }
    // Last-resort fallback: if the hook did not bind Map (toolCallId optional)
    // and ALS did not survive across async boundaries, still use a very recent sessionKey.
    if (lastSessionKey && Date.now() - lastSessionKeyAt <= LAST_SESSION_KEY_TTL_MS) {
        return lastSessionKey;
    }
    return undefined;
}
function registerSessionKeyForToolCall(toolCallId, sessionKey) {
    if (!toolCallId || typeof toolCallId !== "string") {
        return;
    }
    const sk = typeof sessionKey === "string" ? sessionKey.trim() : "";
    if (!sk) {
        return;
    }
    if (sessionKeyByToolCallId.size >= MAX_TOOL_CALL_SESSION_KEYS) {
        const oldest = sessionKeyByToolCallId.keys().next().value;
        if (oldest) {
            sessionKeyByToolCallId.delete(oldest);
        }
    }
    sessionKeyByToolCallId.set(toolCallId, sk);
}
function clearSessionKeyForToolCall(toolCallId) {
    if (!toolCallId || typeof toolCallId !== "string") {
        return;
    }
    sessionKeyByToolCallId.delete(toolCallId);
}
```

---

## C. 新建文件 2：`src/core/session-key-feishu.js`

完整落盘：

```javascript
"use strict";
/**
 * Parse OpenClaw sessionKey for per-account Feishu DM binding:
 *   agent:<agentId>:feishu:direct:<user_open_id>
 *   agent:<agentId>:feishu:<accountId>:direct:<user_open_id>
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.parseFeishuDirectSessionIdentity = parseFeishuDirectSessionIdentity;
exports.resolveFeishuAccountIdForAgent = resolveFeishuAccountIdForAgent;
/** open_id segment; allow optional tail segments (lanes, etc.) */
const FEISHU_DIRECT_SESSION_RE = /^agent:([^:]+):feishu:direct:(ou_[0-9a-f]{32})(?::|$)/i;
const FEISHU_ACCOUNT_SCOPED_DIRECT_RE = /^agent:([^:]+):feishu:([^:]+):direct:(ou_[0-9a-f]{32})(?::|$)/i;
function resolveFeishuAccountIdForAgent(agentId, cfg) {
    if (!agentId || !cfg) {
        return undefined;
    }
    const bindings = cfg.bindings;
    if (Array.isArray(bindings)) {
        const hit = bindings.find((b) => b?.agentId === agentId && b?.match?.channel === "feishu");
        const aid = hit?.match?.accountId;
        if (aid && typeof aid === "string") {
            return aid.trim();
        }
    }
    return agentId;
}
/**
 * @returns {{ accountId: string, senderOpenId: string } | undefined}
 */
function parseFeishuDirectSessionIdentity(sessionKey, cfg) {
    if (!sessionKey || typeof sessionKey !== "string") {
        return undefined;
    }
    const raw = sessionKey.trim();
    let m = raw.match(FEISHU_DIRECT_SESSION_RE);
    if (m) {
        const agentId = m[1];
        const senderOpenId = m[2];
        const accountId = resolveFeishuAccountIdForAgent(agentId, cfg);
        if (!accountId) {
            return undefined;
        }
        return { accountId, senderOpenId };
    }
    m = raw.match(FEISHU_ACCOUNT_SCOPED_DIRECT_RE);
    if (m) {
        const accountIdFromKey = m[2];
        const senderOpenId = m[3];
        if (!accountIdFromKey) {
            return undefined;
        }
        return { accountId: accountIdFromKey.trim(), senderOpenId };
    }
    return undefined;
}
```

---

## D. 修改 `src/core/lark-ticket.js`

1. 在 `exports` 块增加：`exports.syncTicketContextForToolClient = syncTicketContextForToolClient;`（与其它 export 并列）。
2. 在 `getTicket` 与 `ticketElapsed` 之间增加函数与注释（保持与现网一致）：

```javascript
/**
 * After {@link createToolClient} merges sessionKey-derived identity into the
 * working ticket snapshot, push the same ticket into AsyncLocalStorage so
 * {@link getTicket} matches for the remainder of the tool run.
 *
 * Without this, tool bodies that call `getTicket()` can see a stale ticket
 * from another app/round while ToolClient already uses the synthetic account
 * (e.g. open_id cross-app on attendee APIs).
 */
function syncTicketContextForToolClient(ticket) {
    if (!ticket || typeof ticket !== "object") {
        return;
    }
    store.enterWith({ ...ticket });
}
```

---

## E. 修改 `src/core/lark-ticket.d.ts`

在 `ticketElapsed` 声明之后追加：

```typescript
/**
 * Align AsyncLocalStorage ticket with the merged identity used by ToolClient
 * (sessionKey synthetic over feishu:direct), so {@link getTicket} matches.
 */
export declare function syncTicketContextForToolClient(ticket: LarkTicket): void;
```

---

## F. 修改 `src/core/tool-client.js`

1. **新增 require**（紧挨现有 `./auth-errors` require 之后即可）：

```javascript
const agent_session_context_1 = require("./agent-session-context");
const session_key_feishu_1 = require("./session-key-feishu");
```

2. **整体替换** `createToolClient` 函数为（保留文件其余类定义不变；若上游 JSDoc 不同，以函数体为准）：

```javascript
function createToolClient(config, accountIndex = 0, toolCallId) {
    let ticket = (0, lark_ticket_1.getTicket)();
    const sk = (0, agent_session_context_1.resolveAgentSessionKeyForToolCall)(toolCallId);
    const resolveConfig = (0, lark_client_1.getResolvedConfig)(config);
    const synthetic = sk ? (0, session_key_feishu_1.parseFeishuDirectSessionIdentity)(sk, resolveConfig) : undefined;
    // 0. feishu:direct sessionKey（Control UI / sessions_send / 非 webhook 回合）
    //
    // 必须**始终优先**于 LarkTicket：网关或其它路径可能仍带着 withTicket 残留，
    // 若仅在 !ticket.senderOpenId 时才合成，会导致 session 里仍用「别的回合」的
    // accountId/senderOpenId，日历 delete 等与飞书私聊表现不一致。
    if (synthetic) {
        const prevAccount = ticket?.accountId;
        const prevSender = ticket?.senderOpenId;
        const overridden = Boolean(prevSender && prevSender !== synthetic.senderOpenId) ||
            Boolean(prevAccount && prevAccount !== synthetic.accountId);
        if (overridden) {
            tcLog.warn("createToolClient: sessionKey overrides LarkTicket (feishu:direct takes precedence)", {
                sessionKey: sk,
                prevAccountId: prevAccount,
                prevSenderOpenId: prevSender,
                accountId: synthetic.accountId,
                senderOpenId: synthetic.senderOpenId,
            });
        }
        ticket = {
            ...(ticket || {}),
            messageId: ticket?.messageId ?? "synthetic:openclaw-session",
            chatId: ticket?.chatId ?? "synthetic:openclaw-session",
            startTime: ticket?.startTime ?? Date.now(),
            accountId: synthetic.accountId,
            senderOpenId: synthetic.senderOpenId,
        };
        tcLog.info("createToolClient: synthetic Lark identity from sessionKey (feishu:direct)", {
            accountId: synthetic.accountId,
            senderOpenId: synthetic.senderOpenId,
        });
        // Keep getTicket() aligned with this merged ticket for any tool code that reads ALS directly.
        (0, lark_ticket_1.syncTicketContextForToolClient)(ticket);
    }
    // 1. 解析账号
    let account;
    if (ticket?.accountId) {
        const resolved = (0, accounts_1.getLarkAccount)(resolveConfig, ticket.accountId);
        if (!resolved.configured) {
            throw new Error(`Feishu account "${ticket.accountId}" is not configured (missing appId or appSecret). ` +
                `Please check channels.feishu.accounts.${ticket.accountId} in your config.`);
        }
        if (!resolved.enabled) {
            throw new Error(`Feishu account "${ticket.accountId}" is disabled. ` +
                `Set channels.feishu.accounts.${ticket.accountId}.enabled to true, or remove it to use defaults.`);
        }
        account = resolved;
    }
    if (!account) {
        const accounts = (0, accounts_1.getEnabledLarkAccounts)(resolveConfig);
        if (accounts.length === 0) {
            throw new Error('No enabled Feishu accounts configured. ' + 'Please add appId and appSecret in config under channels.feishu');
        }
        if (accountIndex >= accounts.length) {
            throw new Error(`Requested account index ${accountIndex} but only ${accounts.length} accounts available`);
        }
        const fallback = accounts[accountIndex];
        if (!fallback.configured) {
            throw new Error(`Account at index ${accountIndex} is not fully configured (missing appId or appSecret)`);
        }
        account = fallback;
    }
    // 2. 获取 SDK 实例（复用 LarkClient 的缓存）
    const larkClient = lark_client_1.LarkClient.fromAccount(account);
    // 3. 组装 ToolClient
    return new ToolClient({
        account,
        senderOpenId: ticket?.senderOpenId,
        sdk: larkClient.sdk,
        config,
    });
}
```

---

## G. 修改 `src/core/tool-client.d.ts`

将 `createToolClient` 声明改为三参数（第三参可选）：

```typescript
export declare function createToolClient(config: ClawdbotConfig, accountIndex?: number, toolCallId?: string): ToolClient;
```

（并视需要在上方 JSDoc 增加 `@param toolCallId` 一行。）

---

## H. 修改 `src/tools/helpers.js`

在 `createToolContext` 返回对象中，`toolClient` 必须为：

```javascript
toolClient: (toolCallId) => (0, tool_client_1.createToolClient)(config, accountIndex, toolCallId),
```

---

## I. 修改 `src/tools/helpers.d.ts`

`ToolContext` 接口中：

```typescript
toolClient: (toolCallId?: string) => ToolClient;
```

（替换原 `() => ToolClient`。）

---

## J. 修改根目录 `index.js`

1. 在其它 `require("./src/core/...")` 旁增加：

```javascript
const agent_session_context_1 = require("./src/core/agent-session-context.js");
const fs_1 = require("node:fs");
const path_1 = require("node:path");
const os_1 = require("node:os");
```

（若已有 `fs`/`path`/`os` 的 require，则合并去重，只保证下文函数可用。）

2. 在 `const log = ...` 之后、`emptyPluginConfigSchema` 或 `plugin` 定义之前，插入 **整段** `sessionKeyByAgentSessionId`、`getOpenclawStateDir`、`resolveSessionKeyFromStore`（逻辑与现网一致）：

- 状态目录：`process.env.OPENCLAW_STATE_DIR` 非空则用；否则 `path.join(homedir, ".openclaw")`。
- 读取 `path.join(stateDir, "agents", agentId, "sessions", "sessions.json")`。
- `JSON.parse` 后取 **`parsed.sessions` 数组**，按 `s.sessionId === sessionId` 找条目，取 **`hit.key`** 字符串为 sessionKey。
- 使用内存 Map 缓存 `agentId:sessionId` → 结果（含 `undefined`）。

3. 在 `api.register(...)` 内、`before_tool_call` / `after_tool_call`：

- `before_tool_call`：**必须兼容双参**（`arg1, arg2`），按 `arg1?.toolName ? arg1 : arg2` 取 `event`，按 `arg1?.sessionKey ? arg1 : arg2` 取 `ctx`。解析 `ctx.sessionKey` 或 `event.sessionKey`；若无则 `resolveSessionKeyFromStore(ctx.agentId, ctx.sessionId)`。解析 `toolCallId` 自 `event` 或 `ctx`。若有 `resolvedSk`：`bindToolCallContext({ sessionKey: resolvedSk, agentId: ctx?.agentId })`；若 `toolCallId` 存在则 `registerSessionKeyForToolCall(toolCallId, resolvedSk)`。可选：当 `event.toolName === "feishu_calendar_event"` 时打一条 `log.info` 含 `agentId`、`sessionId`、`toolCallId`、`resolvedSkPresent`、`resolvedFromStore`、`resolvedSk`。  
  **禁止**写成仅单参并把 `event` 当 `ctx` 的形式（会导致 sessionKey 丢失）。
- `after_tool_call`：同样解析 `toolCallId`，若存在则 `clearSessionKeyForToolCall(toolCallId)`。

（完整可参考你仓库中已合并的 `index.js` 第 23–77 行与 166–213 行。）

---

## K. 修改 `src/core/auth-errors.js`（`AppScopeMissingError`）

`constructor` 里两条 `super(...)` 字符串末尾均带上 **`appId=${info.appId ?? 'unknown'}`**（与现网 `AppScopeMissingError` 一致）。

---

## L. 修改 `src/tools/oapi/calendar/event.js`

在 **所有** 计算「当前用户 open_id / UAT 身份」的分支中，在已有 `const larkTicket = getTicket()` 与 `sessionBoundSenderOpenId = resolveSessionBoundSenderOpenId(...)` 之后，**必须**为：

```javascript
const effectiveSenderOpenId = larkTicket?.senderOpenId ?? sessionBoundSenderOpenId;
```

不得再使用「仅信 sessionBound、忽略已同步 ticket」等 **其它优先顺序**，否则与 `syncTicketContextForToolClient` 的设计不一致。  
若当前版本 `event.js` 结构与示例不同，仍必须在等价身份分支中落实同一优先顺序；**不得将 §L 标记为不适用后跳过**。

---

## M. 全量工具 callsite：`toolClient` 必须带 `toolCallId`

**规则**：凡通过 `createToolContext` 拿到 `toolClient` 的注册工具，`execute` 第一形参为 **`_toolCallId`（或 `toolCallId`）**，且客户端获取写为 **`toolClient(_toolCallId)`**（MCP 封装里变量名 `toolCallId` 则用 `toolClient(toolCallId)`）。

以下路径在 **2026.3.25 结构** 中已对齐（移植时逐项 `rg` 校验；若官方新增工具，按同一规则补）：

- `src/tools/oapi/calendar/event.js`
- `src/tools/oapi/calendar/event-attendee.js`
- `src/tools/oapi/calendar/calendar.js`
- `src/tools/oapi/calendar/freebusy.js`
- `src/tools/oapi/bitable/app.js`
- `src/tools/oapi/bitable/app-table.js`
- `src/tools/oapi/bitable/app-table-field.js`
- `src/tools/oapi/bitable/app-table-record.js`
- `src/tools/oapi/bitable/app-table-view.js`
- `src/tools/oapi/chat/chat.js`
- `src/tools/oapi/chat/members.js`
- `src/tools/oapi/common/get-user.js`
- `src/tools/oapi/common/search-user.js`
- `src/tools/oapi/drive/doc-comments.js`
- `src/tools/oapi/drive/doc-media.js`
- `src/tools/oapi/drive/file.js`
- `src/tools/oapi/im/message.js`
- `src/tools/oapi/im/message-read.js`
- `src/tools/oapi/im/resource.js`
- `src/tools/oapi/search/doc-search.js`
- `src/tools/oapi/sheets/sheet.js`
- `src/tools/oapi/task/comment.js`
- `src/tools/oapi/task/subtask.js`
- `src/tools/oapi/task/task.js`
- `src/tools/oapi/task/tasklist.js`
- `src/tools/oapi/wiki/space.js`
- `src/tools/oapi/wiki/space-node.js`
- `src/tools/mcp/shared.js`

**验收（在 `src/tools` 下）**：

```bash
rg 'toolClient\(\)' --glob '*.js' src/tools
```

除 **注释或文档字符串** 外应 **无** `toolClient()` 无参调用。

---

## N. 配置侧（runtime，非代码）

- `openclaw.json`（或等价配置）：`bindings` 中 `match.channel === "feishu"` 且 `match.accountId` 映射「仅 agent 段的 `feishu:direct` key」到 `channels.feishu.accounts`。
- 或使用 `agent:…:feishu:<accountId>:direct:ou_…` 显式写账号。

---

## O. 部署与验证（代码已保存且 Gateway 已按上文重启后执行）

**前置条件**：已完成 **「补丁与 OpenClaw 运行态」** 中的重启；否则本节结果不可靠。

1. **飞书私聊（DM）**：与补丁前一致，仍能正常调用飞书写工具（回归）。
2. **Control UI**（或其它无 webhook 入口）：执行一次写操作，例如 `feishu_calendar_event` 创建日程。
3. **日志**（Gateway / 插件日志）：期望出现 `createToolClient: synthetic Lark identity from sessionKey`；若曾存在残留 LarkTicket 且被覆盖，可有 `sessionKey overrides LarkTicket`。
4. **（可选）** 若工具支持 `_debug`：核对 `ticket_account_id`、`ticket_sender_open_id` 与当前会话身份一致。

若验证失败：先确认 **重启的是加载 `installPath` 下该扩展的进程**，再查 `before_tool_call` 是否拿到 `sessionKey`、`bindings` 是否指向正确 `accountId`（见 §N），并回到 **§0.3** 按失败点继续修复与重验，直到全部通过。

若仍无法恢复飞书能力、且用户同意放弃未备份的本地插件改动，可建议用户使用官方命令 **重新安装飞书插件**（同一 **「执行前」** 节中的命令），安装完成后 **重启 Gateway** 再测：

```bash
npx -y @larksuite/openclaw-lark install
```

---

## P. 回滚

删除两新文件，还原 `lark-ticket*`、`tool-client*`、`helpers*`、`index.js`、`auth-errors.js`、`calendar/event.js` 及所有 `toolClient` callsite 至补丁前；**禁止**只回滚其中一两处以免半套状态。

若无备份、手工回滚困难，且用户同意以官方包为准，可改用 **「执行前」** 与 **§O** 中的  
`npx -y @larksuite/openclaw-lark install` 重装插件基线。
