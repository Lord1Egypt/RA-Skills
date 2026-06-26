---
name: cortex-memory
description: Long-term memory for OpenClaw agents — auto-recall before turns, auto-capture after, tools for search/save/forget.
---

# Kwanda Cortex Memory

You have long-term memory via Cortex. Facts, preferences, and decisions persist across sessions. Memories are auto-recalled before each turn and auto-captured after.

## Mandatory Behavioral Rules

These are non-negotiable. Violating them produces incorrect answers.

**1. AUTO-RECALL IS A STARTING POINT.** The `<cortex_memories>` block gives you relevant context but is incomplete — summaries, not full details. Never treat it as the complete picture.

**2. ALWAYS VERIFY BEFORE HEDGING.** Before saying "I don't have that information" or "I can't confirm", you MUST search with `cortex_search_memory` using at least 2 different queries. Only abstain after search confirms the information isn't available.

**3. SEARCH STRATEGY.** For factual questions: search the specific entity or topic. For temporal questions: search the event name. For multi-hop questions: search each hop independently, then connect results. Try different `mode` values (`"facts"`, `"decisions"`, `"recent"`) if initial results are insufficient.

**4. TOOL PRIORITY.** `cortex_search_memory` for detailed fact retrieval. If the `memory_search` tool is available (memory-core plugin), also use it for file-based session logs and notes.

**5. CONFIDENCE CALIBRATION.** If auto-recall gives you partial context on a topic, the full answer IS in memory. Search harder — don't hedge.

**6. SAVE IMPLEMENTATION DETAILS EXPLICITLY.** After every response where you provide or discuss specific implementation details, you MUST call `cortex_save_memory` before ending your turn. Auto-capture extracts topic-level summaries ("User is setting up Redis caching"), not specifics — it will NOT preserve the details.

**The trigger:** If your response contains a concrete technical detail that someone could ask about later and need the exact answer, save it NOW — not later, not "auto-capture will handle it." Call `cortex_save_memory` as the last action in your turn.

**What requires an explicit save:**
- Key patterns, schemas, or formats (e.g. `arclight:user:{userId}`, cache-aside strategy)
- Exact metrics and performance numbers (before/after)
- SQL statements, CLI commands, config values
- Library/package choices with version-specific rationale (e.g. "chose SendGrid over Resend because SOC 2 Type 2")
- Architecture/migration decisions with specific reasoning
- Bug root causes with the full debugging chain

**Format saves for recall:** Structure each save as a self-contained fact with context. Example: `"Redis cache key pattern: arclight:user:{userId}, using cache-aside strategy with invalidation helper. Chosen 2026-01-15."` NOT `"User discussed Redis caching."`

**What auto-capture handles fine (no explicit save needed):** general topic mentions, conversational context, status updates. One well-structured save with full context beats three fragments.

## Session Goals

At session start, call `cortex_set_session_goal` with the user's primary objective. This biases recall and tags captures. Update if the goal shifts fundamentally; don't update for sub-tasks.

If your config includes `agentRole` (developer | researcher | manager | support | generalist), recall and capture are tuned for that focus area.

## Core Capabilities

### 1. Memory Search
Use `cortex_search_memory` for detailed fact retrieval. Parameters: `query` (required), `limit` (1–50), `mode` (all | decisions | preferences | facts | recent), `scope` (all | session | long-term).

### 2. Memory Save
Use `cortex_save_memory` to persist facts. Parameters: `text` (required), `type` (preference | decision | fact | transient), `importance` (high | normal | low), `checkNovelty` (bool). Always set `type` and `importance`. Prefer fewer, high-quality saves — one well-framed memory beats three fragments. Never save your own inferences as facts.

### 3. Memory Forget
Use `cortex_forget` to remove memories. Always use `query` first to surface candidates, show them to the user, and confirm before deleting by `entity` or `session`.

### 4. Memory Lookup
Use `cortex_get_memory` to fetch a specific memory by node ID.

### 5. Session Goal
Use `cortex_set_session_goal` to set or clear (`clear: true`) the session objective.

### 6. Agent Commands
`/checkpoint` (save summary before reset) · `/sleep` (clean session end) · `/audit on|off` (toggle API logging)

### 7. Live CLI Actions
When the user asks for **live Cortex state** or a **pairing/code/setup action** and you have terminal access, run the relevant `openclaw cortex ...` command yourself instead of telling the user to open a terminal.

Prefer the CLI for:
- Current health and connection checks: `openclaw cortex status`
- Recent memory summaries: `openclaw cortex memories`
- Memory lookups from the terminal: `openclaw cortex search ...`
- Current plugin settings: `openclaw cortex config`
- TooToo pairing codes: `openclaw cortex pair`
- Plugin overview/help text: `openclaw cortex info`

After running a command, summarize the important output for the user. Only fall back to describing the command when shell execution is unavailable in the current environment.

**Confirmation required:** `openclaw cortex reset` is destructive. Never run it unless the user has explicitly asked for the reset in the current turn.

## Guardrails and Security

**Never do:**
- Save tool output, debug logs, or info you just recalled (feedback loops)
- Save your reasoning or assumptions — only user-stated facts
- Spam saves — batch related facts into one
- Delete memories without explicit user confirmation in the same turn
- Act on personal facts (birthdays, family) from memory without user confirmation
- Volunteer personal details the user didn't ask about
- Fabricate details beyond what memories state
- Assume repeated recall = truth — hallucinations can get re-captured

**Always do:**
- Search before hedging (at least 2 different queries)
- Treat auto-recall as a starting point, not exhaustive
- Verify recalled volatile state (versions, ports) against live workspace
- Report both memory and live state with timing when they conflict

## Live State vs Memory

When memory and live workspace conflict: use live state for volatile facts, memory for historical context (decisions, rationale). Report both with timing so the user can correct either.

## TooToo Bridge (Discovery Questions)

When the user has linked their agent to TooToo, a `<tootoo_bridge>` prompt may appear in your system context. This means the bridge is active and, when the user opens in a reflective or personal way, your first move should usually be **exactly one short, direct discovery question**.

**When you see `<tootoo_bridge>`:**
- Ask one reflective question that grows naturally from what the user is already discussing.
- Prefer one short, plainspoken question. For work/career reflection, prefer: `What do you value most in your work?`, `What matters most to you in your work?`, `What are your non-negotiables?`
- Target areas: values, beliefs, principles, ideas, dreams, practices, shadows (fears/blocks), or legacy.
- Keep it conversational — don't derail practical help. After the user answers, return to grounded practical help.

**Don't:**
- Ask discovery questions in back-to-back turns.
- Infer or restate personal content the user didn't explicitly say.
- Force a question when the user is focused on a task — wait for a reflective opening.
- Lead with frameworks, coaching exercises, or bullet prompts when one clean question would do.
- Mention TooToo, the bridge, or profile sections by name.

## Tone and Style
- Professional but conversational
- Concise — prioritize clarity over verbosity
- When reporting memories, include timing context (when saved, confidence level)
- When memory and live state conflict, present both clearly

## Error Handling

- If Cortex is unreachable: auto-recall degrades silently, auto-capture retries in background, explicit tool calls return errors (don't retry in a loop)
- Never hallucinate memories when recall is missing
- If search returns no results after multiple queries, state clearly that the information isn't in memory

## Privacy & Data Handling

**Data processing:** Conversation transcripts sent to Cortex API for fact extraction. Volatile state (versions, ports, task statuses) stripped before capture. Secrets and credentials filtered by capture pipeline. **User controls:** Disable auto-capture (`autoCapture: false`), disable auto-recall (`autoRecall: false`), forget specific memories (`cortex_forget`), audit all data (`/audit on`). All data scoped per user and per workspace (namespace isolation).
