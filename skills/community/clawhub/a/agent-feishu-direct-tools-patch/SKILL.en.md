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

# openclaw-lark: Agent Direct Tool Invocation Without Feishu Ticket (Full Patch Skill)

**Execution convention**: The paths below are relative to the **`openclaw-lark` extension root** (the directory containing `index.js` and `src/`). Before editing code, the implementing Agent **must complete "Before execution: explain to the user and wait for confirmation"** and receive **explicit user consent**, then modify code in **§B–§M** order and run the **acceptance commands** at the end, achieving **semantic equivalence** with the validated implementation below.  
**Mandatory requirement**: Do not skip any section simply because "the current version structure is different / same-named snippets were not found"; you must find semantically equivalent locations in the current code and apply the same changes (see **§0.3 Strict Execution and Closed-Loop Acceptance Protocol**).

- Verified on Feishu plugin code structures corresponding to **2026.3.18** and **2026.3.25**.
- **Upgrade risk**: If the official Feishu plugin later changes plugin directories, `before_tool_call` shape, `execute` signatures, or core module names, paths/patch points in this document may become invalid; after upgrade, re-check item by item and re-run smoke tests (Control UI + Feishu DM).

Do **not** mix-read this Skill with other Skills; this document is self-contained.

---

## Before execution: explain to the user and wait for confirmation (Agent's top priority, before §B–§M)

**Before creating/modifying any source file (starting from §B)**, the implementing Agent **must first** send a **pre-patch briefing** to the user (any current channel is fine: Feishu, Control UI, IDE chat, etc.), then continue only after the user is informed and gives **explicit confirmation**. Do not modify code when the user is only browsing, asking questions, or has not clearly stated agreement.

### What the briefing should include (Agent should phrase naturally as needed)

1. **What will be done**: This Skill will **batch-modify the `openclaw-lark` extension** by sections (create 2 files, change core modules and many tool files), to resolve identity/account issues for "agent direct Feishu tool calls without webhook ticket" (overview in **§A**).
2. **How to execute**: Follow **§B–§M** in order; after edits, the user must **restart OpenClaw Gateway** for changes to take effect (see **"Patch and OpenClaw Runtime State"**); validation is in **§O**.
3. **Risks**: Environment/version differences may cause merge conflicts or patch-point mismatch; after Feishu plugin upgrades, re-check against the version notes at the beginning of this Skill.
4. **Recommendation**: Before starting, **back up** the directory pointed to by `plugins.installs.openclaw-lark.installPath` in `openclaw.json`, or use **git** commits/branches for rollback.
5. **If failed or Feishu is still unavailable after patch**: First **roll back** manual changes per **§P**; if still abnormal and you want to restore the **official installable baseline**, and the user **understands and accepts potential overwrite of local edits**, run the official install command (requires local Node/npx):

```bash
npx -y @larksuite/openclaw-lark install
```

Reinstall follows the published flow of **@larksuite/openclaw-lark** and **may overwrite manual edits in that plugin directory**; ask the user to confirm before running. After reinstall, still follow OpenClaw docs to **enable plugin and restart Gateway**.

6. **One-time Skill**: If this Skill is loaded into OpenClaw skill list, use it **short-term** only; see **§0.2**.

### When code editing can start

- **Required**: The user explicitly states agreement to execute this patch (e.g., "confirm execution", "start patching", "agree, modify according to Skill"; interpret equivalent expressions by locale).
- **Forbidden**: User only says "explain this Skill" / "what is this patch" without confirmation -> **explain only, do not edit files**.
- After confirmation, start from **§B**; throughout execution, still follow §0 completion reporting and restart notes in **"Patch and OpenClaw Runtime State"**.

---

## 0. Completion and user notification (mandatory for implementing Agent)

This section applies to **Agents in AI-assisted development tools** (e.g., Cursor, GitHub Copilot, Codeium, Windsurf), **Agents in OpenClaw chat**, and **any implementing Agent executing this Skill**. After **all code changes in §B–§M are complete** (including `rg` acceptance in §M when runnable), you **must** send the user **one clear completion message** (Feishu reply, Control UI reply, or current chat channel), including at least:

1. **Result status**: completed / partially completed (and where blocked) / no file edits (consultation only).
2. **Which files were changed**: list paths item by item (relative to **`openclaw-lark` extension root**) and mark **added** or **modified**, e.g.:
   - Added: `src/core/agent-session-context.js`, `src/core/session-key-feishu.js`
   - Modified: `src/core/lark-ticket.js`, `src/core/lark-ticket.d.ts`, `src/core/tool-client.js`, `src/core/tool-client.d.ts`, `src/tools/helpers.js`, `src/tools/helpers.d.ts`, `index.js`, `src/core/auth-errors.js`, `src/tools/oapi/calendar/event.js`, and each `toolClient(_toolCallId)` tool file listed in §M (if you changed files beyond this list, include them too).
3. **What categories of adjustments were made** (short user-facing summary, no large code dump), e.g.: added session context + sessionKey parsing, synthesized Lark ticket and ALS sync, added `toolCallId` to `createToolClient`, bound sessionKey in plugin hooks, calendar identity prioritizes `getTicket()`, auth errors include `appId`, and full tool `toolCallId` pass-through.
4. **Gateway restart reminder (mandatory)**: explain that **disk changes do not take effect until OpenClaw Gateway (or the Node process loading the plugin) is restarted**; ask user to **restart in their environment** (if implementing Agent is not explicitly authorized/capable, **do not claim you already restarted for user**).
5. **Optional follow-up**: remind user to run Feishu DM + Control UI smoke tests per **§O** after restart; if Skill was temporarily loaded into OpenClaw skill directory, remove it per **§0.2** to avoid persistent loading.
6. **If execution failed or Feishu is still abnormal after patch**: remind user to try rollback per **§P** first; if still unavailable, and user accepts "official reinstall may overwrite local edits", run  
   `npx -y @larksuite/openclaw-lark install` (consistent with **"Before execution: explain to user and wait for confirmation"**), then restart Gateway.

---

## 0.2 One-time patch: how to avoid "staying permanently" in OpenClaw skill list

This Skill is a **one-time engineering patch used on demand**, not a business skill for daily always-on dialogue. Recommended usage below avoids it **appearing long-term in selectable skills** and interfering with other Agents:

| Practice | Description |
|------|------|
| **Use local AI tools only; do not load in OpenClaw** | Put `agent-feishu-direct-tools-patch` under **skills/rules/context** directories supported by your tool, or run by **@mention/pasting `SKILL.md` path** in chat; **do not** write it into `openclaw.json` `skills`. This way OpenClaw Gateway runtime **cannot see** this Skill at all. |
| **Temporarily load into OpenClaw** | If runtime **Gateway Agent** must read this doc: **temporarily** copy this directory into an existing folder under `skills.load.extraDirs`; **delete the copy after use** (or remove the extra directory added specifically for this patch), then **restart Gateway**. If it no longer appears in list, normal state is restored. |
| **Do not keep `enabled: true` long-term** | If config has `skills.entries.<name>`: do **not** keep this Skill permanently enabled; enable only when patching (if your OpenClaw version supports per-entry toggle), then switch back to **disabled** or remove the entry. |
| **Do not rely on "Agent auto-selects skill"** | Trigger explicitly with **one clear user sentence** (e.g., "apply openclaw-lark agent-feishu-direct-tools-patch"), avoiding mixing patch skill with daily always-on sets like `team-agent-onboarding`. |
| **Distribute via repo or archive** | Include the whole `agent-feishu-direct-tools-patch` directory in Git or package for reuse; whether runtime loads it is separate from whether files stay on disk — keeping files != must enable permanently in `skills.entries`. |

**Relation to §"Allow OpenClaw chat Agent to load this Skill"**: those items describe how to load when **short-term needed**; by default, still prefer **execute in AI-assisted dev tools + do not keep loaded in Gateway after use**, or **temporary load -> remove immediately after patch**.

---

## 0.3 Strict execution and closed-loop acceptance protocol (must be followed by implementing Agent)

This section prevents "executed but missed/wrong/skipped changes." After user confirmation, implementing Agent must follow this closed loop until all pass:

1. **Build section by section**: execute in **§B->§M** order; self-check immediately after each section; do not perform one coarse batch and patch later.
2. **No section skipping**: no section (including **§L**) may be marked "not applicable" due to version differences; if code structure differs, locate semantically equivalent positions in current implementation and apply equivalent changes.
3. **Dual validation** per section:  
   - **Text/structure validation** (key symbols, function signatures, call forms, exports);  
   - **Behavior-intent validation** (whether target semantics are satisfied, not only string presence).
4. **Fix-on-failure**: if any validation fails, continue modifying and re-validating; do not close in "partially passed" state.
5. **Completion gate (all required)**:  
   - Every section §B–§M passes;  
   - No-arg `toolClient()` check in §M passes (excluding comments/docs contexts);  
   - Targeted re-check of high-risk points: `index.js` hook arg compatibility, `createToolClient(config, accountIndex, toolCallId)` 3-arg chain, and `effectiveSenderOpenId` priority in `calendar/event.js`.
6. **Evidence-based completion report**: completion message must include "section acceptance checklist", with at least one concrete evidence line per §B–§M (e.g., matched function/signature/call form), not only "done".
7. **No completion without full green**: if environment limits prevent validating some item, status must be "not completed / pending validation" and continue with processable items; do not claim "patch completed."

---

## Patch and OpenClaw runtime state (required reading for AI tools and Gateway)

### Why Gateway restart is mandatory (or equivalent process restart)

- OpenClaw **loads plugins (including `openclaw-lark`) into Node process when Gateway starts**; editing disk `.js` files does **not** hot-replace loaded modules.
- **Saving files != live effect**. After §B–§M edits, you must **restart the process loading this plugin**, then patch effects appear in **Feishu / Control UI / sessions_send**.

### Recommended operation order (implementer should follow)

1. **Confirm you edit the runtime-used directory**: `openclaw.json` -> `plugins.installs.openclaw-lark.installPath` (or your actual enabled extension directory) must match the current **`openclaw-lark` root** being edited; editing a mismatched copy will still run old code after restart.
2. **Save all related files** (including the two new `src/core/*.js`).
3. **Restart OpenClaw Gateway** (or any Node process hosting `openclaw` and loading plugins):
   - **Foreground run**: stop process in Gateway terminal (e.g., Ctrl+C), then start with your normal command (e.g., `openclaw gateway` or project doc command).
   - **Daemon/systemd/Docker/remote Gateway**: restart the **same service on the machine actually running Gateway** (consistent with official "restart Gateway after plugin config changes").
4. **Run validation in §O** (test Feishu DM + Control UI once each).

### Using this Skill in AI-assisted development tools

- Agent/human edits code per §B–§M -> **must execute step 3 above (restart Gateway)** -> then validate.  
- If restart is skipped, you may misjudge as "patch ineffective."

### Allow OpenClaw chat Agent to "load" this Skill as well (optional, short-term recommended)

The Skill directory in this repo is `agent-feishu-direct-tools-patch/` (contains `SKILL.md`). By default OpenClaw **does not** auto-scan subdirectories inside Feishu extension; if runtime Agent needs to read this temporarily, choose one:

1. **Copy** (preferred over symlink for easy full-directory deletion after patch) the whole `agent-feishu-direct-tools-patch` into one directory already listed in `skills.load.extraDirs` in `openclaw.json`, so `.../agent-feishu-direct-tools-patch/SKILL.md` exists. After patching, **delete the copy** and restart Gateway; see **§0.2**.
2. Or **temporarily add** one path in `skills.load.extraDirs` pointing to a parent directory containing only this Skill; **remove from config after use** and restart Gateway.
3. If using `skills.entries`: do **not** keep this Skill entry permanently `enabled: true`; enable only when executing patch, then disable afterward (behavior depends on OpenClaw version; follow docs).

Note: **plugin code patch** and **exposing SKILL to runtime Agent** are two separate things—former edits `openclaw-lark` source + restart to take effect; latter only exposes **instructions** to Agent and **cannot replace** source changes and restart. **Default recommendation: execute this Skill in local AI-assisted dev tools**, to avoid patch docs being permanently loaded in Gateway skill list (**§0.2**).

---

## A. Problem to solve

| Type | Description |
|------|------|
| Entry path | Control UI, sessions_send, etc. are **non-webhook** paths with no complete `LarkTicket`. |
| Account | `createToolClient` falls back to default account -> **misuses main**, etc.; error shows **wrong appId**. |
| Identity | OpenClaw already has `sessionKey` (`agent:...:feishu:...:direct:ou_...`) but not in tool stack -> cannot select account + senderOpenId. |
| ALS mismatch | Synthesized ticket not written back to ALS -> stale `getTicket()` -> **open_id cross-app** (calendar attendee, etc.). |
| Hook boundary | Missing `toolCallId`, `(event,ctx)` order differences, ALS loss across `await` -> need **Map + short TTL lastSessionKey**. |

**Target behavior**: `sessionKey -> parse accountId/senderOpenId -> synthesize ticket (priority over stale LarkTicket) -> syncTicketContextForToolClient -> ToolClient consistent with getTicket -> all tools use toolClient(toolCallId)`.**

---

## B. Add new file 1: `src/core/agent-session-context.js`

Write exactly the following file:

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

## C. Add new file 2: `src/core/session-key-feishu.js`

Write exactly:

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

## D. Modify `src/core/lark-ticket.js`

1. Add in `exports` block: `exports.syncTicketContextForToolClient = syncTicketContextForToolClient;` (parallel with other exports).
2. Add the following function and comment between `getTicket` and `ticketElapsed` (keep consistent with current production implementation):

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

## E. Modify `src/core/lark-ticket.d.ts`

Append after `ticketElapsed` declaration:

```typescript
/**
 * Align AsyncLocalStorage ticket with the merged identity used by ToolClient
 * (sessionKey synthetic over feishu:direct), so {@link getTicket} matches.
 */
export declare function syncTicketContextForToolClient(ticket: LarkTicket): void;
```

---

## F. Modify `src/core/tool-client.js`

1. **Add require** (right after existing `./auth-errors` require):

```javascript
const agent_session_context_1 = require("./agent-session-context");
const session_key_feishu_1 = require("./session-key-feishu");
```

2. **Replace entire** `createToolClient` function with (keep other class definitions unchanged; if upstream JSDoc differs, function body prevails):

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

## G. Modify `src/core/tool-client.d.ts`

Change `createToolClient` declaration to three parameters (third optional):

```typescript
export declare function createToolClient(config: ClawdbotConfig, accountIndex?: number, toolCallId?: string): ToolClient;
```

(And optionally add one `@param toolCallId` line in JSDoc above.)

---

## H. Modify `src/tools/helpers.js`

In the object returned by `createToolContext`, `toolClient` must be:

```javascript
toolClient: (toolCallId) => (0, tool_client_1.createToolClient)(config, accountIndex, toolCallId),
```

---

## I. Modify `src/tools/helpers.d.ts`

In `ToolContext` interface:

```typescript
toolClient: (toolCallId?: string) => ToolClient;
```

(Replace original `() => ToolClient`.)

---

## J. Modify root `index.js`

1. Add near other `require("./src/core/...")`:

```javascript
const agent_session_context_1 = require("./src/core/agent-session-context.js");
const fs_1 = require("node:fs");
const path_1 = require("node:path");
const os_1 = require("node:os");
```

(If `fs`/`path`/`os` requires already exist, merge/deduplicate; just ensure functions below are available.)

2. After `const log = ...` and before `emptyPluginConfigSchema` or `plugin` definition, insert the **full block**: `sessionKeyByAgentSessionId`, `getOpenclawStateDir`, `resolveSessionKeyFromStore` (logic must match production):

- State dir: use `process.env.OPENCLAW_STATE_DIR` if non-empty; otherwise `path.join(homedir, ".openclaw")`.
- Read `path.join(stateDir, "agents", agentId, "sessions", "sessions.json")`.
- After `JSON.parse`, read **`parsed.sessions` array**, locate `s.sessionId === sessionId`, take **`hit.key`** string as sessionKey.
- Use in-memory Map cache for `agentId:sessionId` -> result (including `undefined`).

3. Inside `api.register(...)`, in `before_tool_call` / `after_tool_call`:

- `before_tool_call`: **must support dual args** (`arg1, arg2`), use `arg1?.toolName ? arg1 : arg2` for `event`, and `arg1?.sessionKey ? arg1 : arg2` for `ctx`. Resolve from `ctx.sessionKey` or `event.sessionKey`; if missing, use `resolveSessionKeyFromStore(ctx.agentId, ctx.sessionId)`. Resolve `toolCallId` from `event` or `ctx`. If `resolvedSk` exists: `bindToolCallContext({ sessionKey: resolvedSk, agentId: ctx?.agentId })`; if `toolCallId` exists then `registerSessionKeyForToolCall(toolCallId, resolvedSk)`. Optional: when `event.toolName === "feishu_calendar_event"`, log one `log.info` including `agentId`, `sessionId`, `toolCallId`, `resolvedSkPresent`, `resolvedFromStore`, `resolvedSk`.  
  **Forbidden** to write as single-arg form and treat `event` as `ctx` (will lose sessionKey).
- `after_tool_call`: resolve `toolCallId` similarly; if present, `clearSessionKeyForToolCall(toolCallId)`.

(For full reference, see merged `index.js` in your repo around lines 23–77 and 166–213.)

---

## K. Modify `src/core/auth-errors.js` (`AppScopeMissingError`)

In `constructor`, append **`appId=${info.appId ?? 'unknown'}`** to both `super(...)` strings (same as current production `AppScopeMissingError`).

---

## L. Modify `src/tools/oapi/calendar/event.js`

In **all** branches calculating "current user open_id / UAT identity", after existing `const larkTicket = getTicket()` and `sessionBoundSenderOpenId = resolveSessionBoundSenderOpenId(...)`, it **must** be:

```javascript
const effectiveSenderOpenId = larkTicket?.senderOpenId ?? sessionBoundSenderOpenId;
```

Do not use other priority orders like "sessionBound only, ignore synced ticket"; otherwise it is inconsistent with `syncTicketContextForToolClient` design.  
If current `event.js` structure differs from sample, still implement the same priority in semantically equivalent identity branches; **do not mark §L as not applicable and skip**.

---

## M. Full tool callsite sweep: `toolClient` must pass `toolCallId`

**Rule**: For any registered tool obtaining `toolClient` via `createToolContext`, `execute` first parameter must be **`_toolCallId` (or `toolCallId`)**, and client retrieval must be **`toolClient(_toolCallId)`** (in MCP wrapper where variable name is `toolCallId`, use `toolClient(toolCallId)`).

The following paths are aligned in **2026.3.25 structure** (during porting, validate each with `rg`; if official adds tools, apply same rule):

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

**Acceptance (under `src/tools`)**:

```bash
rg 'toolClient\(\)' --glob '*.js' src/tools
```

Except **comments or doc strings**, there should be **no** no-arg `toolClient()` calls.

---

## N. Configuration side (runtime, not code)

- In `openclaw.json` (or equivalent): in `bindings`, `match.channel === "feishu"` and `match.accountId` maps "agent-only `feishu:direct` key" to `channels.feishu.accounts`.
- Or use explicit account form: `agent:...:feishu:<accountId>:direct:ou_...`.

---

## O. Deploy and validate (run after code is saved and Gateway restarted as above)

**Prerequisite**: Restart in **"Patch and OpenClaw Runtime State"** has been completed; otherwise results here are unreliable.

1. **Feishu DM**: same as before patch; Feishu write tools still work (regression check).
2. **Control UI** (or other non-webhook entry): perform one write operation, e.g., create event with `feishu_calendar_event`.
3. **Logs** (Gateway/plugin logs): expect `createToolClient: synthetic Lark identity from sessionKey`; if stale LarkTicket existed and was overridden, may see `sessionKey overrides LarkTicket`.
4. **(Optional)** if tool supports `_debug`: verify `ticket_account_id`, `ticket_sender_open_id` consistent with current session identity.

If validation fails: first confirm **you restarted the process that loads extension under `installPath`**, then check whether `before_tool_call` receives `sessionKey` and whether `bindings` points to correct `accountId` (see §N), then return to **§0.3** and continue fix/re-validate until all pass.

If Feishu capability still cannot be restored and user agrees to discard unbacked local plugin edits, suggest official command to **reinstall Feishu plugin** (same command as in **"Before execution"** section); after install, **restart Gateway** and test again:

```bash
npx -y @larksuite/openclaw-lark install
```

---

## P. Rollback

Delete the two new files, restore `lark-ticket*`, `tool-client*`, `helpers*`, `index.js`, `auth-errors.js`, `calendar/event.js`, and all `toolClient` callsites to pre-patch state; **do not** roll back only one or two points to avoid half-patched state.

If no backup and manual rollback is difficult, and user agrees to use official package baseline, use the reinstall command in **"Before execution"** and **§O**:  
`npx -y @larksuite/openclaw-lark install`
