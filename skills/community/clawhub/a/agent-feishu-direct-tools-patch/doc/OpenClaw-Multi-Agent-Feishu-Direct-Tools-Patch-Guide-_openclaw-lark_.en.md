# Agent Direct Feishu Tool Patch (openclaw-lark)

> [!NOTE]
> An English Skill file is provided: `SKILL.en.md` (same content, English language). If needed, you can rename it to `SKILL.md` to replace the current Chinese version.

This document is the maintainer-facing companion to the `agent-feishu-direct-tools-patch` SKILL.  
It keeps the original patch rationale and code touchpoints, and adds execution constraints, acceptance loop, restart requirements, and usage guidance in Cursor/OpenClaw chats.

Applicable extension root: `extensions/openclaw-lark/` (if your fork/path differs, map by relative structure).

---

## 1. Background and Goals

A typical real-world scenario is **multi-agent collaboration in OpenClaw**:
the user gives instructions to a primary agent in Feishu chat, then the primary agent dispatches work to a sub-agent via `sessions_send` inside OpenClaw (for example, creating a calendar event).

This dispatch path usually does not go through Feishu inbound webhook again, so the sub-agent may not have a fresh/full Feishu ticket at tool runtime.  
With default fallback behavior, tool calls can fall back to the primary agent app context or a default account, causing identity-permission mismatch:
**the sub-agent executes the task, but auth resolves to the primary agent's app user context**.

If the primary agent lacks a specific Feishu tool permission (for example calendar write scope), calls fail with permission errors even when the sub-agent actually has the required permission.  
This also causes identity confusion across the call chain and harder troubleshooting.

The goal of this patch is: on **Control UI / `sessions_send` / non-webhook** paths, Feishu tool calls should use the **current executing agent's app user identity** first, so that:

- the correct Feishu sub-app/account (`accountId`) is selected;
- the `open_id` stays in the correct app context;
- cross-app `open_id` issues (for example attendee APIs) are avoided;
- permission misalignment and identity confusion in multi-agent dispatch flows are resolved.

Core flow:

`sessionKey -> accountId + senderOpenId -> synthetic ticket -> sync ALS -> ToolClient aligned with getTicket`

---

## 2. Typical Issues and Root Causes

### 2.1 Common Symptoms

- User asks the primary agent in Feishu chat; the primary agent dispatches to a sub-agent through `sessions_send`.
- The sub-agent executes Feishu tools, but auth falls back to primary/default account identity.
- The sub-agent actually has permission, but calls still fail with `no permission / missing scope / appId mismatch`.
- Feishu DM path works, but Control UI calls such as `feishu_calendar_event` fail.
- Error messages point to the wrong `appId` (often fallback to `main`).
- Or `open_id` cross-app inconsistency appears.

### 2.2 Root Cause Breakdown

1. `LarkTicket` is mainly injected in webhook inbound flow; Control UI often lacks it.
2. `createToolClient` may fall back to default account or primary-agent-related context when ticket identity is missing.
3. OpenClaw already has `sessionKey` (for example `agent:...:feishu:...:direct:ou_...`), but legacy flow does not fully propagate it into tool runtime, so current executing agent identity cannot be reconstructed reliably.
4. Even with a synthetic ticket, if ALS is not updated with `enterWith`, tool code calling `getTicket()` may still read stale identity, causing ToolClient/runtime identity divergence.

---

## 3. Solution Overview (Architecture Level)

| Layer | What it does |
|------|--------|
| `index.js` | Bind and clear session context in `before_tool_call` / `after_tool_call`; support both `(event, ctx)` and `(ctx, event)`; optionally resolve `sessionKey` from `sessions.json`. |
| `agent-session-context.js` | ALS + `toolCallId -> sessionKey` map + short-TTL `lastSessionKey` fallback. |
| `session-key-feishu.js` | Parse both `feishu:direct` and `feishu:<accountId>:direct` sessionKey patterns. |
| `tool-client.js` | `createToolClient(config, accountIndex, toolCallId)`; prioritize sessionKey-derived identity over stale ticket; sync merged ticket back to ALS. |
| `lark-ticket.js` | Add `syncTicketContextForToolClient` to keep `getTicket()` consistent with ToolClient identity. |
| `helpers.js` + OAPI/MCP | Pass through `toolCallId` via `toolClient(toolCallId)` across callsites. |
| `calendar/event.js` | Use `effectiveSenderOpenId = getTicket()?.senderOpenId ?? sessionBoundSenderOpenId`. |
| `auth-errors.js` | Include `appId=` in `AppScopeMissingError` for multi-account troubleshooting. |

---

## 4. Key Change List (Synchronized with SKILL)

The following aligns with `agent-feishu-direct-tools-patch/SKILL.md`:

- Add `src/core/agent-session-context.js`
  - `bindToolCallContext`, `registerSessionKeyForToolCall`, `resolveAgentSessionKeyForToolCall`, etc.
- Add `src/core/session-key-feishu.js`
  - `parseFeishuDirectSessionIdentity`, `resolveFeishuAccountIdForAgent`.
- Update `src/core/lark-ticket.js` and `src/core/lark-ticket.d.ts`
  - Add `syncTicketContextForToolClient(ticket)`.
- Update `src/core/tool-client.js` and `src/core/tool-client.d.ts`
  - 3-arg signature: `createToolClient(config, accountIndex = 0, toolCallId)`.
  - sessionKey identity takes precedence, then sync merged ticket to ALS.
- Update `src/tools/helpers.js` and `src/tools/helpers.d.ts`
  - `toolClient: (toolCallId) => createToolClient(config, accountIndex, toolCallId)`.
- Update root `index.js`
  - dual-arg hook compatibility; bind/clear session context; `sessions.json` fallback resolution.
- Update `src/core/auth-errors.js`
  - include `appId` in `AppScopeMissingError`.
- Update `src/tools/oapi/calendar/event.js`
  - unify `effectiveSenderOpenId` priority.
- Update all relevant tool callsites
  - `execute(_toolCallId, params)` + `toolClient(_toolCallId)` across OAPI and `src/tools/mcp/shared.js`.

---

## 5. Execution Rules (From SKILL, Added)

### 5.1 Explicit Pre-Execution Confirmation

Before editing source files, clearly explain to the operator:

- which files/categories will be changed;
- risks and rollback options;
- that Gateway restart is mandatory.

Proceed only after explicit confirmation.

### 5.2 Ordered Execution and Closed Acceptance Loop

- Apply changes section by section (no skipping, no partial-only patching).
- For each section, validate both structure/signature and intended behavior.
- If any check fails, keep fixing; do not close as "partially done".
- Final report should include changed files, change categories, and pending items (if any).

### 5.3 Mandatory Restart Reminder

- These are filesystem edits; runtime modules are not hot-replaced automatically.
- Restart OpenClaw Gateway (or the Node process that loads this plugin) before validation.

### 5.4 Failure Fallback

- Roll back using the rollback checklist first.
- If still broken and user accepts overwrite risk, reinstall official plugin baseline:
  - `npx -y @larksuite/openclaw-lark install`

---

## 6. sessionKey and Config Conventions

- Supported sessionKey patterns:
  - `agent:<agentId>:feishu:direct:ou_<32hex>`
  - `agent:<agentId>:feishu:<accountId>:direct:ou_<32hex>`
- In `openclaw.json` (or equivalent), `bindings` should include:
  - `bindings[].match.channel === "feishu"`
  - `bindings[].match.accountId` mapped to `channels.feishu.accounts.<accountId>`
- In multi-account setup, ensure app auth/scope are correct per user per app; use `appId=` in errors for precise diagnosis.

---

## 7. How to Use This SKILL in Cursor and Similar AI Dev Tools (Added)

Recommended for one-time patch execution, re-apply after merge conflicts, and post-upgrade porting checks.

### 7.1 Recommended Flow

1. Give a clear instruction: apply patch according to `agent-feishu-direct-tools-patch/SKILL.md`.
2. Ask the agent for a pre-execution brief; confirm explicitly.
3. Let the agent apply sectioned changes and return a file-level report.
4. Restart Gateway.
5. Run DM + Control UI smoke tests (see section 9).

### 7.2 Best Practices

- Use as a temporary/one-off task skill, not always-on default skill.
- Create a Git commit/branch or backup before patching.
- After `openclaw-lark` upgrades, re-check key signatures before reuse (especially hook shapes, `createToolClient`, `execute` signatures).

---

## 8. How to Use It Directly in OpenClaw Chat (Added)

If you want runtime OpenClaw agents to read this SKILL, use it temporarily:

1. Put `agent-feishu-direct-tools-patch/` under a directory scanned by `skills.load.extraDirs` (copy is recommended for easy cleanup).
2. Trigger explicitly in chat, for example:
   - "Apply `agent-feishu-direct-tools-patch` to patch `openclaw-lark`."
3. You can also send the skill archive file directly to the OpenClaw bot in Feishu chat; the bot will automatically read and execute the workflow instructions.
4. After execution, remove the temporary skill copy or disable the entry.
5. Restart Gateway so this patch skill does not remain as daily-chat noise.

Note: exposing SKILL to runtime agents only provides instructions; it does **not** replace actual code edits and restart.

---

## 9. Deployment and Validation

1. Save all source changes.
2. Restart Gateway / the Node process hosting OpenClaw.
3. In Control UI (same agent and session context), test write operations such as calendar creation.
4. Check logs:
   - `createToolClient: synthetic Lark identity from sessionKey`
   - if override happens: `sessionKey overrides LarkTicket`
5. If `_debug` is available, verify consistency of `ticket_account_id`, `ticket_sender_open_id`, and `user_open_id`.

---

## 10. Rollback and Troubleshooting

### 10.1 Rollback Recommendation

- Back up key files beforehand:
  `src/core/lark-ticket.js`, `src/core/lark-ticket.d.ts`, `src/core/tool-client.js`, `src/core/tool-client.d.ts`, `index.js`, `src/tools/helpers.js`, `src/tools/helpers.d.ts`, `src/tools/oapi/calendar/event.js`, plus the two new core files.
- Roll back as a full set to avoid half-patched state.

### 10.2 Troubleshooting Checklist

| Symptom | Check |
|------|--------|
| Still resolves to `main` `appId` | Did `before_tool_call` receive `sessionKey`? Did `parseFeishuDirectSessionIdentity` match? Is `bindings` mapping correct? |
| cross-app / open_id mismatch | Is `syncTicketContextForToolClient` actually called? Is any tool still reading stale cached identity? |
| Hook seems ineffective | Is `before_tool_call` registered? Is dual-arg order compatibility implemented correctly? |
| `sessions.json` fallback fails | Current logic expects `parsed.sessions[]` entries with `sessionId/key`; for legacy formats, extend parser or ensure gateway passes `ctx.sessionKey`. |

---

## 11. Division of Responsibility with SKILL Doc

- `SKILL.md`: execution manual for agents (what to change, in what order, how to validate).
- This document: design/maintenance/operations context for human maintainers and reviewers (why, where, deployment, rollback).
- An English Skill file is provided: `SKILL.en.md` (same content, English language). If needed, you can rename it to `SKILL.md` to replace the current Chinese version.

Use both together: **agents execute by SKILL; maintainers review by this document**.

---

*Content follows the repository's current implementation. For cross-branch porting, verify with `git diff` against file paths and function signatures.*

