# Step 4: Metadata Wiring + Auto-Continue in `agent-session.ts`

**File:** `packages/coding-agent/src/core/agent-session.ts`
**Four injection points** (4a–4d)

## 4a. Imports

Add after existing imports:

```typescript
import { consumePendingTobeContext, getRef, logAction, _tobeLog } from "./playfilo-db.js";
```

## 4b. Metadata Provider in Constructor

In the `AgentSession` constructor, after setting up instance variables (cwd, model registry, etc.) but **before** subscribing to agent events, register a lazy callback that the `_persist` shim calls on each write to capture the agent's current state:

```typescript
this.sessionManager.setMetadataProvider(() => ({
  systemPrompt: this.agent.state.systemPrompt || null,
  model: this.agent.state.model
    ? { provider: this.agent.state.model.provider, modelId: this.agent.state.model.id }
    : null,
  thinkingLevel: this.agent.state.thinkingLevel ?? "off",
  tools: (this.agent.state.tools ?? []).map((t) => ({
    name: t.name,
    description: (t as any).description ?? "",
  })),
}));
```

**Why:** The _persist shim (step 3e) stores agent config alongside each DAG node. This callback provides live model/tool state without `_persist` needing to know about `AgentSession` internals.

## 4c. SESSION_SWITCH Logging in `switchSession()`

Find the `switchSession()` method. Wrap the existing `setSessionFile` call with HEAD capture and action logging:

```typescript
const previousHead = getRef("PI_HEAD");
this.sessionManager.setSessionFile(sessionPath);
this.agent.sessionId = this.sessionManager.getSessionId();
const newHead = getRef("PI_HEAD");
if (newHead) {
  logAction("SESSION_SWITCH", previousHead, newHead,
    JSON.stringify({ trigger: "human", session: sessionPath }));
}
```

**Why:** When the user switches sessions via Pi's UI, the DAG's HEAD jumps to a different lineage. `trace()` with `filter_mode: "switches"` shows these events, helping the agent understand cross-session navigation.

## 4d. Deferred Context Replacement in Auto-Continue Handler

In `_processAgentEvent()`, find the existing auto-continue block that fires on `agent_end` when there are queued messages. It may look like:

```typescript
if (event.type === "agent_end") {
  // ... existing auto-continue logic ...
}
```

Add the tobe auto-continue handler **before** the existing `agent_end` retry/compaction block:

```typescript
// --- PLAYFILO: Tobe auto-continue (must run before retry/compaction) ---
// setTimeout(0) is safe here: by the time _processAgentEvent(agent_end) runs,
// all stale events (tool_result + aborted assistant) have already been processed
// through the event queue. The follow-up queue is intact because runLoop exits
// via the stopReason==="aborted" return BEFORE reaching getFollowUpMessages().
// setTimeout(0) fires at the first event loop yield, ensuring the continuation
// starts before any post-prompt cleanup (e.g. subscription teardown).
if (event.type === "agent_end" && this.agent.hasQueuedMessages()) {
    const tobeCtx = consumePendingTobeContext();
    if (tobeCtx) {
        setTimeout(() => {
            this.agent.replaceMessages(tobeCtx);
            this.agent.continue().catch(() => {});
        }, 0);
        return; // Skip retry/compaction — tobe takes over
    }
}
```

**Why setTimeout(0) is safe:** When the tobe tool fires `agent.abort()` inside `executeToolCalls`, the inner loop iterates once more (because `hasMoreToolCalls` is still `true` from the tobe tool_call). On that next iteration, `streamAssistantResponse()` is called with the aborted signal, returns `stopReason === "aborted"`, and `runLoop` exits via `return` — **before** reaching `getFollowUpMessages()`. The follow-up queue stays intact.

By the time `_processAgentEvent(agent_end)` runs (via the event queue), both stale events (tool_result + aborted assistant) have already been processed. `replaceMessages()` is safe to call without delay.

**Why not in the tool handler:** The tool handler runs inside `executeToolCalls`, which is mid-loop. Calling `replaceMessages()` there would be overwritten by the stale `appendMessage()` calls that follow (tool_result emit, aborted assistant emit).

## 4e. Defensive Null Checks for DAG-Loaded Entries

DAG-loaded entries (via `loadEntriesFromDAG`) may lack fields Pi's native code expects. Several places in `agent-session.ts` need guards:

**Footer metrics:** Find where `assistantMsg.content` and `assistantMsg.usage` are accessed for footer display. Add optional chaining:

```typescript
// Before (crashes on DAG entries):
assistantMsg.content.filter(...)
// After:
assistantMsg.content?.filter(...)

// Before:
const cost = assistantMsg.usage.cost;
// After:
if (assistantMsg.usage) {
  const cost = assistantMsg.usage.cost;
  // ...
}
```

**Post-compaction checks:** Find where `assistant.usage` is accessed after compaction. Guard with:

```typescript
if (assistant.usage) {
  // ... usage-related logic ...
}
```

These are defensive — they prevent crashes when the session manager loads DAG entries that don't carry Pi's internal fields (`usage`, `api`, `stopReason`, etc.).

## Verify

```bash
cd packages/coding-agent && npm run build
```

At this point, the full integration loop is wired:
1. Agent state captured → `_persist` shim → DAG nodes with metadata
2. Session switches logged in action_log
3. Tobe context replacement happens after stale events are consumed
4. DAG-loaded entries don't crash Pi's footer/compaction code
