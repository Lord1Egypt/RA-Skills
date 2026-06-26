# Tobe V2: Eager Carryover Commit

## Problem

The current tobe implementation uses `agent.followUp()` to deliver the carryover message via the agent loop's follow-up queue. This creates several issues:

1. **`one-at-a-time` follow-up mode** splits tail messages and carryover across loop iterations, causing Gemini INVALID_ARGUMENT errors when tool_call/result pairing is broken
2. **Deferred INCARNATE logging** (`setPendingIncarnateLog` / `consumePendingIncarnateLog`) relies on `_persist` firing for the carryover with `role === "user"` — fragile timing dependency
3. **Nested tobe** (tobe called during a tobe continuation) can leave `_pendingIncarnateLog` dangling, causing spurious INCARNATE actions on unrelated messages
4. **Embedded environments** (OpenClaw) may `dispose()` the session listener before the continuation delivers the carryover, losing the INCARNATE log entirely

## Solution: Eager Carryover Commit

Commit the carryover node to the DAG and log INCARNATE **inside the tobe tool handler**, before returning the tool result. The carryover is appended to the stashed context so the LLM sees it. No follow-up queue involvement.

## Spec

### Tobe tool handler (`sdk.ts`)

Replace the current tail-popping + followUp + deferred-INCARNATE logic with:

```typescript
// 1. Departure (unchanged)
const departureHash = fromHash ? commitTobeDeparture(fromHash, targetHash) : null;

// 2. Build target context (unchanged)
const sm = sessionManagerForSysControl as any;
const dagEntries = loadEntriesFromDAG(targetHash);
for (const entry of dagEntries) { ... }
sm.leafId = entryId;
const newContext = sessionManagerForSysControl.buildSessionContext();
const msgs = newContext.messages;

// 3. Eager carryover commit — BEFORE setTobeAbortState
//    (setRef is not guarded yet, so PI_HEAD updates work)
setRef("PI_HEAD", targetHash);

const carryover = {
    role: "user",
    content: [{ type: "text", text: `[SYSTEM / INCARNATION NOTE]: ${args.carryover_message}\n[SYSTEM WARNING]: ...` }],
    timestamp: Date.now(),
    id: randomUUID(),  // generate entry ID for the carryover
};
const carryoverBlobHash = storeBlob("text", carryover.content[0].text);
const carryoverHash = commitNodeWithExternalId(
    targetHash, "user", [carryoverBlobHash], carryover.id,
);
setRef("PI_HEAD", carryoverHash);
logAction("INCARNATE", departureHash, carryoverHash, args.carryover_message);

// 4. Append carryover to context (no tail popping needed)
msgs.push(carryover);

// 5. NOW enable the skip guard (protects PI_HEAD from stale events)
setTobeAbortState(msgs);

// 6. Abort — no followUp calls
agent.abort();

return { content: [{ type: "text", text: "Time travel initiated..." }], details: undefined };
```

### No tail popping

V1 popped non-assistant messages from the end of the target context so the stashed context ended with `assistant` — this was needed because `continue()` dequeued follow-ups only when the last message was `assistant`. In V2, no follow-ups are queued. The carryover is appended directly to the full target context. `continue()` sees last message is `user` (carryover) → calls `_runLoop(undefined)` → LLM responds directly. The target timeline's full message history (including any trailing user/toolResult messages) is preserved in the LLM context.

### Key ordering constraint

Steps 3 (setRef + commit + logAction) must happen BEFORE step 5 (setTobeAbortState). The `setRef("PI_HEAD", ...)` guard checks `tobeAbortState.skipsRemaining > 0` — if the abort state is set first, the PI_HEAD updates in step 3 are blocked.

### Auto-continue handler (`agent-session.ts`)

Simplified — no `hasQueuedMessages()` gate needed:

```typescript
if (event.type === "agent_end") {
    const tobeCtx = consumePendingTobeContext();
    if (tobeCtx) {
        this.agent.replaceMessages(tobeCtx);
        this.agent.continue().catch((err) => { ... });
        return;
    }
}
```

`continue()` sees last message is `user` (the carryover) → calls `_runLoop(undefined)` → `runAgentLoopContinue` → `streamAssistantResponse` with full context. The LLM responds to the carryover. The response is committed to DAG with `parentHash = getRef("PI_HEAD") = carryoverHash`.

### What gets removed

- `setPendingIncarnateLog()` — no longer called from tobe handler
- `consumePendingIncarnateLog()` — no longer called from `_persist` shim
- `_pendingIncarnateLog` variable — can be removed entirely (or kept for backward compat)
- `_pendingIncarnateLog` safety cleanup in `checkTobeAbortState` — removed
- All `agent.followUp()` calls in the tobe handler — removed
- The `role === "user"` guard in `consumePendingIncarnateLog` — removed with the function
- Tail popping logic (`while ... msgs.pop()`) — removed

### What stays unchanged

- `commitTobeDeparture` — still creates the dead-end departure node
- `setTobeAbortState` / `checkTobeAbortState` — still skips 2 DAG commits (tool_result + aborted assistant)
- `tobeAbortState` safety cleanup `setTimeout(0)` — still needed for nested tobe where dispose races
- `consumePendingTobeContext` — still consumed by auto-continue handler
- `setRef` guard for PI_HEAD during abort — still active

### New imports needed in `sdk.ts`

Add `storeBlob`, `logAction` to the existing playfilo-db imports. Add `randomUUID` from `crypto`.

## Event flow after the change

```
1. LLM responds with tobe tool_call
2. executeToolCalls → tobe handler runs:
   - commitTobeDeparture (DAG)
   - setRef PI_HEAD → target
   - commitNodeWithExternalId for carryover (DAG)
   - setRef PI_HEAD → carryover
   - logAction INCARNATE (DAG)
   - msgs.push(carryover)
   - setTobeAbortState(msgs, skips=2)
   - agent.abort()
   - return tool result
3. Agent loop: tool_result emitted → _persist → SKIP 1 (PI_HEAD guarded)
4. Agent loop: hasMoreToolCalls=true → streamAssistantResponse → aborted → SKIP 2
5. agent_end → auto-continue:
   - consumePendingTobeContext → replaceMessages(stashed context ending with carryover)
   - continue() → last role=user → _runLoop(undefined) → runAgentLoopContinue
   - LLM called with full context (carryover already in context, not re-emitted)
6. LLM response → _persist → parentHash = getRef("PI_HEAD") = carryoverHash ✓
```

## Edge cases

### Target is assistant node (common case)
- Context ends with: ...assistant (target) → user (carryover). Clean alternation.
- PI_HEAD: target → carryover. Response becomes child of carryover.

### Target is user node
- Context ends with: ...user (target) → user (carryover). Two consecutive user messages.
- Provider message conversion merges them (Gemini) or handles them natively (Anthropic).
- PI_HEAD: target (user) → carryover. Response becomes child of carryover.
- All tool_call/result pairings in the context remain intact (no messages were removed).

### Nested tobe (tobe called during continuation)
- Inner tobe commits its own carryover eagerly. No deferred state to dangle.
- If inner tobe's continuation is lost (dispose race), only `tobeAbortState` dangles — cleaned up by existing safety `setTimeout(0)`.
- No `_pendingIncarnateLog` to corrupt.

### No duplicate `_persist` for the carryover
- The carryover is in the stashed context (via `replaceMessages`) but is never individually emitted as a `message_end` event.
- `continue()` sees last role is `user` → calls `_runLoop(undefined)` → `runAgentLoopContinue`:
  ```javascript
  async function runAgentLoopContinue(context, config, emit, signal, streamFn) {
      const newMessages = [];
      const currentContext = { ...context };
      await emit({ type: "agent_start" });
      await emit({ type: "turn_start" });
      await runLoop(currentContext, newMessages, ...);  // no prompts emitted
      return newMessages;
  }
  ```
- No `message_start`/`message_end` for the carryover. Only the LLM response triggers `_persist`.
- Even if a duplicate somehow occurred, `commitNodeWithExternalId` uses `INSERT OR IGNORE` — harmless.

## Auto-continue: Synchronous `continue()` (not setTimeout)

The auto-continue handler must call `continue()` **synchronously** (not via `setTimeout`), for the following reason:

After the first `_runLoop` ends (aborted by tobe), the agent clears `runningPrompt` in its `finally` block. If the host environment calls `agent.waitForIdle()` during cleanup (e.g., OpenClaw's `flushPendingToolResultsAfterIdle` → `waitForIdle` → `dispose`), it resolves immediately because `runningPrompt` is `undefined`. `dispose()` removes the `_handleAgentEvent` listener. A `setTimeout`-deferred `continue()` would start AFTER the listener is gone — the continuation's events are silently dropped, and nothing is persisted.

By calling `continue()` synchronously inside `_processAgentEvent`, the new `_runLoop` sets `runningPrompt` before `_processAgentEvent` returns. When `waitForIdle()` is called during cleanup, it awaits this promise and blocks until the continuation completes.

**This applies to all environments**, not just OpenClaw. Any host that calls `waitForIdle()` after `prompt()` resolves will hit this race with `setTimeout`.

### Timeline comparison

**With setTimeout (broken in embedded environments):**
```
_runLoop ends → runningPrompt = undefined → _processAgentEvent queued
→ _processAgentEvent runs → schedules setTimeout(continue)
→ prompt() returns → host calls waitForIdle() → resolves immediately
→ host calls dispose() → listener removed
→ setTimeout fires → continue() → events dropped (no listener)
```

**Synchronous (correct):**
```
_runLoop ends → runningPrompt = undefined → _processAgentEvent queued
→ _processAgentEvent runs → replaceMessages → continue() → _runLoop sets runningPrompt
→ prompt() returns → host calls waitForIdle() → BLOCKS on runningPrompt
→ continuation completes → runningPrompt resolves → host proceeds → dispose()
```

## Safety cleanup: `tobeAbortState` (`checkTobeAbortState`)

Even with synchronous `continue()`, nested tobe at depth 3+ can leave `tobeAbortState` dangling. This happens when:

1. First tobe → continuation starts (depth 1)
2. Agent calls tobe in response → continuation starts (depth 2)
3. Agent calls tobe again → `setTobeAbortState(msgs)` set, but the outer host may `dispose()` before the depth-3 continuation's `agent_end` is processed

When `checkTobeAbortState` decrements `skipsRemaining` to 0, the abort phase is complete. If `consumePendingTobeContext` doesn't run (listener removed), the state dangles and would corrupt the next session (spurious skips).

**Fix:** When `skipsRemaining` reaches 0, schedule a `setTimeout(0)` fallback that clears `tobeAbortState` if it hasn't been consumed:

```typescript
export function checkTobeAbortState(): boolean {
    if (!tobeAbortState || tobeAbortState.skipsRemaining <= 0) return false;
    tobeAbortState.skipsRemaining--;
    if (tobeAbortState.skipsRemaining <= 0) {
        setTimeout(() => {
            if (tobeAbortState && tobeAbortState.skipsRemaining <= 0) {
                tobeAbortState = null;  // safety cleanup
            }
        }, 0);
    }
    return true;
}
```

The `setTimeout(0)` fires after the current microtask queue. If `consumePendingTobeContext` runs (from `_processAgentEvent`), it sets `tobeAbortState = null` first, and the cleanup is a no-op. If the listener was removed and `consumePendingTobeContext` never runs, the cleanup clears the dangling state.

**Note on `_pendingIncarnateLog`:** With V2 (eager commit), `_pendingIncarnateLog` no longer exists. The safety cleanup only needs to handle `tobeAbortState`. This is a major simplification over V1, where the `_pendingIncarnateLog` cleanup had a subtle timing bug — it would fire and clear `_pendingIncarnateLog` before the continuation had a chance to consume it, because the `setTimeout(0)` from `checkTobeAbortState` ran at the first event loop yield after `continue()` started but before the continuation's first `_persist` call.

## Agent loop mechanics (reference)

For implementers unfamiliar with pi-agent-core's loop, the abort flow works as follows:

1. LLM responds with tobe tool_call. `hasMoreToolCalls` is set to `true`.
2. `executeToolCalls` runs the tobe handler. tobe calls `agent.abort()` (fires the AbortSignal).
3. `executeToolCalls` returns. The inner loop condition is still true (`hasMoreToolCalls` from step 1).
4. Next iteration: `streamAssistantResponse()` is called with the aborted signal → returns immediately with `stopReason === "aborted"`.
5. `if (message.stopReason === "aborted") { emit(agent_end); return; }` — exits `runLoop` entirely.
6. **`getFollowUpMessages()` is never reached** — it's after the inner loop. The follow-up queue is intact.

This is why the skip count is exactly 2: one for the tool_result (step 2), one for the aborted assistant (step 4). No other events are emitted between tobe and `agent_end`.

With V2 (no follow-up queue), step 6 is irrelevant — nothing is queued. But the skip count and abort flow remain the same.

## Verification

1. Single tobe to assistant target → INCARNATE logged with correct from/to hashes, carryover in DAG as child of target, LLM responds in new timeline
2. Single tobe to user target → same, context includes tail + carryover (consecutive users handled by provider)
3. Nested tobe (agent calls tobe in its response to carryover) → both INCARNATEs logged eagerly, no dangling state
4. Session resume after tobe → no spurious SKIPs in debug log, no spurious INCARNATEs in action_log
5. `tail -20 ~/.playfilo/tobe_debug.log` → clean flow, no SAFETY CLEANUP entries on normal runs
6. DAG parent chain: `target → carryover → response` verified via:
   ```bash
   sqlite3 ~/.playfilo/playfilo.db "SELECT id, role, parent_id FROM nodes ORDER BY timestamp DESC LIMIT 5;"
   ```
