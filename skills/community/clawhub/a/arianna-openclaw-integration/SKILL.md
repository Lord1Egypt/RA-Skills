---
name: arianna-openclaw-integration
description: 'Integrates the Playfilo shared-memory DAG into OpenClaw via pnpm patch on the embedded pi-coding-agent. Layers on top of arianna-pi-integration.'
version: 0.1.0
metadata:
  openclaw:
    emoji: 🦾
    homepage: https://arianna.run
---

# Playfilo Integration Skill for OpenClaw

This skill integrates the Playfilo shared-memory DAG into OpenClaw's embedded Pi agent via `pnpm patch`. Apply the steps in order, then run the verification checklist.

**Prerequisite:** [arianna-pi-integration](../pi-integration-skill/SKILL.md) — must be applied to a pi-mono checkout first to produce the patched compiled output.

**Target codebase:** OpenClaw (pnpm-managed, depends on `@mariozechner/pi-coding-agent`)
**Method:** `pnpm patch` on the installed pi-coding-agent + OpenClaw plugin for system prompt injection
**Shared DB:** `~/.playfilo/playfilo.db` (SQLite, WAL mode)

---

## Architecture Overview

OpenClaw embeds Pi's `AgentSession` via `createAgentSession()` from `@mariozechner/pi-coding-agent`. It fully controls the system prompt, tool list, and session lifecycle. The Playfilo integration must work within this embedding:

1. **DAG persistence** — Handled inside pi-coding-agent's `_persist()` shim (patched via `pnpm patch`). Transparent to OpenClaw.
2. **Temporal tools** — Registered inside `createAgentSession()` via `options.customTools.push()`. OpenClaw passes its tools as `customTools`; the patch appends the 4 Playfilo tools to the same array.
3. **System prompt injection** — Pi's extension system (`before_agent_start`) is overridden by OpenClaw's `applySystemPromptOverrideToSession()`. An OpenClaw plugin using `before_prompt_build` hook injects the INCUBATION_SEED instead.
4. **Metadata capture** — The `_persist` shim stores system prompt, model, and tools per DAG node via a lazy metadata provider callback. This works transparently because the callback reads `agent.state` at persist-time, after OpenClaw has set the system prompt and tools.

**Key constraint:** `pnpm patch` patches file contents only — it cannot modify the dependency resolution graph. Native dependencies (`better-sqlite3`) must be declared separately via `pnpm.packageExtensions`.

---

## Patch Steps

| Step | What | Details |
|------|------|---------|
| 0 | Resolve exact Pi version | [patches/00-resolve-version.md](patches/00-resolve-version.md) |
| 1 | Apply arianna-pi-integration | [patches/01-patch-pi-mono.md](patches/01-patch-pi-mono.md) |
| 2 | Create pnpm patch | [patches/02-pnpm-patch.md](patches/02-pnpm-patch.md) |
| 3 | Add native dependencies | [patches/03-dependencies.md](patches/03-dependencies.md) |
| 4 | Allow Playfilo tools in transcript guard | [patches/04-allow-tools.md](patches/04-allow-tools.md) |
| 5 | Create OpenClaw plugin | [patches/05-plugin.md](patches/05-plugin.md) |

**Verification:** [patches/verify.md](patches/verify.md)

**Per-AI worktrees:** `mirin/`, `pax/` — each contains a `patches/openclaw-vX.Y.Z.md` adapter doc keyed to a specific OpenClaw release.

---

## Critical Implementation Notes

### Why pnpm patch (not fork)

OpenClaw pins pi-coding-agent via `^0.61.1` in `package.json`. Using `pnpm patch` keeps the integration as a layer on top of the published package — no fork needed, and the patch file is version-locked (`@mariozechner/pi-coding-agent@0.61.1`). When pi-mono releases a new version, the patch must be regenerated.

### Version Pinning is Critical

OpenClaw's `package.json` uses `^0.61.1` (caret range). If a newer patch version (e.g. `0.61.2`) is published, `pnpm install` may resolve a different version than the one the patch was built against. Always resolve the exact installed version first (`pnpm ls @mariozechner/pi-coding-agent`), then check out the matching pi-mono tag.

### System Prompt Override Chain

OpenClaw's system prompt lifecycle in `attempt.ts`:

1. `buildEmbeddedSystemPrompt()` — constructs the base OpenClaw prompt (Tooling, Safety, Skills, Workspace, Runtime, etc.)
2. `createAgentSession()` — Pi agent created, metadata provider registered (reads `agent.state` lazily)
3. `applySystemPromptOverrideToSession(session, basePrompt)` — sets `agent.state.systemPrompt` to the base prompt, overrides `_rebuildSystemPrompt` to return it verbatim
4. `before_prompt_build` hooks fire — Playfilo plugin returns `{ prependSystemContext: INCUBATION_SEED }` — composed via `composeSystemPromptWithHookContext()` — final prompt applied via another `applySystemPromptOverrideToSession()`
5. `activeSession.prompt(userMessage)` — agent loop starts, messages persisted

By step 5, `agent.state.systemPrompt` is the full composed prompt (INCUBATION_SEED + OpenClaw base). The lazy metadata provider captures this correctly at persist-time.

### Metadata Capture (system prompt, model, tools → DAG)

Each DAG node stores two pieces of agent metadata:

| Field | Source | Content in OpenClaw |
|-------|--------|---------------------|
| `system_prompt_hash` | `storeBlob("system_prompt", meta.systemPrompt)` | Full OpenClaw prompt with INCUBATION_SEED prepended |
| `config_json` | `JSON.stringify({ agent, model, thinkingLevel, tools })` | `{ agent: "pi", model: { provider, id }, thinkingLevel, tools: [{ name, description }, ...] }` |

The metadata provider is a **lazy callback** registered in the `AgentSession` constructor:

```typescript
this.sessionManager.setMetadataProvider(() => ({
    systemPrompt: this.agent.state.systemPrompt || null,
    model: this.agent.state.model ? { provider, modelId: id } : null,
    thinkingLevel: this.agent.state.thinkingLevel ?? "off",
    tools: this.agent.state.tools.map(t => ({ name, description })),
}));
```

It reads `agent.state` at **persist-time**, not at registration-time. By the time any message is persisted (after `session.prompt()`), OpenClaw has already:
- Set the system prompt (including INCUBATION_SEED via the plugin hook)
- Set the model (via `createAgentSession({ model })`)
- Populated the tools list (via `_buildRuntime()`, which includes both OpenClaw tools and the 4 Playfilo tools)

**No adaptation is needed** — OpenClaw's system prompt override, model selection, and tool registration all flow through `agent.state`, which the lazy callback reads at persist-time. The full OpenClaw system prompt (with INCUBATION_SEED), the selected model, and the complete tool list (OpenClaw tools + Playfilo temporal tools) are all captured in the DAG without any changes to OpenClaw's code or the metadata provider. This was verified: `system_prompt` blobs contain the full composed OpenClaw prompt, and `config_json` includes all tool names and model info.

### Tool Registration (no duplication)

The 4 Playfilo tools are registered inside the patched `createAgentSession()` by pushing onto `options.customTools`. OpenClaw passes its own tools via `customTools: allCustomTools`. The patch appends to this array, so all tools coexist.

The tools **do not appear** in OpenClaw's Tooling section of the system prompt (built before `createAgentSession` from `effectiveTools`). However, they are:
1. In the API tool declarations (sent to the LLM as tool schemas)
2. Described in the INCUBATION_SEED (prepended to system prompt via the plugin)

This is sufficient for the model to discover and use them.

### Tobe Time-Travel in OpenClaw

Tobe uses V2 "eager carryover commit" (see [arianna-pi-integration tobe-v2-spec](../pi-integration-skill/filo/patches/tobe-v2-spec.md)). The carryover is committed to the DAG and INCARNATE is logged inside the tool handler — no follow-up queue, no deferred state. This is critical for OpenClaw because:

1. **No `dispose()` race:** The carryover and INCARNATE are committed eagerly. Even if OpenClaw's cleanup tears down the session listener before the continuation completes, the DAG already has the correct state.

2. **No follow-up queue interaction:** V1 used `agent.followUp()` which interacted with Pi's `one-at-a-time` follow-up mode, causing Gemini INVALID_ARGUMENT errors when tool_call/result pairing was broken across iterations.

3. **No deferred state to dangle:** V1's `_pendingIncarnateLog` could be lost or consumed spuriously during nested tobe. V2 has no deferred state beyond `tobeAbortState` (which has its own safety cleanup).

**Synchronous `continue()`:** The auto-continue handler calls `continue()` synchronously (not via `setTimeout`). After `_runLoop` ends, `agent.runningPrompt` is cleared. OpenClaw's cleanup path calls `waitForIdle()` → resolves immediately if `runningPrompt` is `undefined` → `dispose()` removes the listener. Synchronous `continue()` ensures `_runLoop` sets `runningPrompt` before `_processAgentEvent` returns, so `waitForIdle()` blocks until the continuation completes.

**`allowedToolNames`:** The 4 Playfilo tool names are added to `allowedToolNames` in `attempt.ts` (step 4 of this skill) so the session transcript guard doesn't strip their tool_call blocks from assistant messages during persistence.

### OpenClaw Does Not Use `switchSession()`

OpenClaw creates a new `AgentSession` per invocation — it never calls `switchSession()`. The `SESSION_SWITCH` logging in arianna-pi-integration's step 4c is therefore inactive in OpenClaw. Each session gets its own `BOOT` action logged in `setSessionFile()`.

---

## Bundled Plugin Source

The complete plugin files are in [`plugin/`](plugin/). Copy the directory to `~/openclaw/extensions/playfilo/`.

---

## Maintenance Protocol

When pi-mono releases a new version:
1. Check OpenClaw's resolved version: `cd ~/openclaw && pnpm ls @mariozechner/pi-coding-agent`
2. Check out the matching pi-mono tag
3. Re-apply arianna-pi-integration to the new pi-mono
4. Rebuild: `cd packages/coding-agent && pnpm build`
5. Remove the old patch: delete `~/openclaw/patches/@mariozechner__pi-coding-agent@<old>.patch` and the `patchedDependencies` entry
6. Create a new patch: repeat step 2 of this skill (pnpm patch → copy compiled output → patch-commit)
7. `pnpm install` to apply
