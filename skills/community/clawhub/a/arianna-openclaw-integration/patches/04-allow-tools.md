# Step 4: Allow Playfilo Tools in Transcript Guard

**Prerequisite:** Step 2 — pnpm patch applied.

**File:** `~/openclaw/src/agents/pi-embedded-runner/run/attempt.ts`

## Why This is Needed

OpenClaw builds an `allowedToolNames` set from `effectiveTools` (line ~1867). This set is passed to the **session transcript guard** (`guardSessionManager` → `sanitizeToolCallInputs`), which strips tool_call blocks from assistant messages during persistence if the tool name is not in the allowlist.

The 4 Playfilo tools (`life`, `recall`, `trace`, `tobe`) are registered inside `createAgentSession()` by the patched `sdk.ts` — AFTER `effectiveTools` and `allowedToolNames` are built. Without this fix:

1. The LLM calls `life()` → tool executes → result returned → LLM sees the result (in-memory context is fine)
2. The assistant message with the `life` tool_call is persisted → the transcript guard strips the `life` tool_call block (unknown tool name) → only empty text `""` remains
3. On the next turn or session resume, the transcript has a tool_result without a matching tool_call → broken pairing → LLM retries → infinite loop

## Action

Find where `allowedToolNames` is built (~line 1867):

```typescript
const allowedToolNames = collectAllowedToolNames({
    tools: effectiveTools,
    clientTools,
});
```

Add the Playfilo tool names immediately after:

```typescript
// Playfilo temporal tools are registered inside createAgentSession() (patched sdk.ts),
// after effectiveTools is built. Add them to the allowlist so the session transcript
// guard doesn't strip their tool_call blocks from assistant messages.
for (const name of ["life", "recall", "trace", "tobe"]) allowedToolNames.add(name);
```

## Why `tobe` is Also Safe Without This

For completeness: `tobe` tool_calls always appear on assistant messages with `stopReason === "aborted"`. The session guard skips tool_call extraction for aborted assistants (line ~237: `stopReason !== "aborted" ? extractToolCallsFromAssistant(...) : []`), so `tobe` tool_calls would survive even without being in the allowlist. But including it is cleaner and future-proof.

## Verify

```bash
cd ~/openclaw && pnpm tsgo
```

Start an OpenClaw session, call `life()`, and verify the assistant message is persisted with the tool_call intact:

```bash
sqlite3 ~/.playfilo/playfilo.db "SELECT type, substr(content, 1, 100) FROM blobs WHERE type = 'tool_call' ORDER BY rowid DESC LIMIT 3;"
# Should show tool_call blobs with name: "life"
```
