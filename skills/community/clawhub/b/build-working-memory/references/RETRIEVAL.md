# Retrieval Workflow

How the agent decides what to load, in what order, and how much.

---

## Core Principle: Budget-Aware Layered Loading

The agent has a finite context window. Memory loading must be strategic, not
exhaustive. The system uses a **four-phase approach** where each phase is
progressively more expensive and only triggered when needed.

```
Phase 1: Orient       →  state.json                ~200 tokens, always
Phase 2: Anchor       →  resumption.md             ~300 tokens, always
Phase 3: Context      →  MEMORY.md + threads.md + events.json    ~1500-2200 tokens, conditional
Phase 4: Deep Recall  →  daily logs + archive + targeted event lookup       variable, on-demand
```

Total baseline cost (Phases 1-2): ~500 tokens
Typical session cost (Phases 1-3): ~2000 tokens
Heavy retrieval (all phases): ~4000-6000 tokens

The goal is to stay in Phases 1-3 for 80% of sessions.

---

## Phase 1: Orient

**Always runs. Cost: ~200 tokens. Time: instant.**

Read `memory/state.json` and extract:

```
├── How long since last session? (hours/days)
├── Which threads are active?
├── Are there pending flags?
│   ├── memory_review_due → schedule curation in Phase 3
│   ├── threads_need_update → prioritize threads.md loading
│   └── archive_candidates_exist → low priority, handle at session end
├── What was the last topic position?
└── What conversation style is expected?
```

**Decision outputs from Phase 1:**
- `time_gap`: hours since last session → determines how much context to reload
- `active_thread_ids`: which threads to load in Phase 3
- `flags`: which maintenance tasks to weave into the session
- `style_hint`: how to calibrate tone before the conversation starts

### Time Gap Heuristic

| Gap             | Loading Strategy                                        |
|-----------------|---------------------------------------------------------|
| < 2 hours       | Light. Skip Phase 3, go straight to conversation.       |
| 2 - 24 hours    | Standard. Run Phases 1-3.                               |
| 1 - 7 days      | Full reload. Run Phases 1-3, preload last 3 daily logs. |
| 7+ days         | Deep reload. All phases. Load weekly summaries if they exist. Treat resumption.md with some skepticism — context may have shifted. |

---

## Phase 2: Anchor

**Always runs. Cost: ~300 tokens.**

Read `memory/resumption.md` in full.

This is the subjective continuity bridge. The agent reads it as a first-person
narrative and adopts its framing as a starting mental state. Unlike other files,
resumption.md is consumed holistically — not parsed for specific data.

**What the agent should extract (implicitly, not mechanically):**
- Where we left off
- What's likely to happen next
- What to watch for
- What tone to match

**Important**: If `time_gap` > 7 days, treat resumption.md as potentially stale.
Still read it for historical context, but don't anchor to its predictions.

---

## Phase 3: Context

**Conditional. Cost: ~1000-2000 tokens.**

This phase has two branches depending on the incoming signal.

### Branch A: Continuing a Known Thread

Triggered when: the user's opening message references a known active thread,
or the resumption note predicts continuation.

```
1. Load the specific thread from threads.md (skip others)
2. Check thread's "Open Questions" — any that match the user's message?
3. If the thread references specific daily logs or structured events, note them for potential Phase 4
4. Load relevant section of MEMORY.md ("About This Project" etc.)
5. If the question is event- or date-sensitive, load top matching records from events.json
```

**Do NOT load**: unrelated threads, full MEMORY.md, any daily logs yet.

### Branch B: New or Ambiguous Topic

Triggered when: the user's opening message doesn't map to any active thread,
or the agent can't determine intent from Phases 1-2 alone.

```
1. Load MEMORY.md in full (Active + Fading sections)
2. Load all thread headers from threads.md (title + status + current position only)
3. If the message contains obvious entities, dates, purchases, meetings, issues, or "which happened first" wording, also load/rank from events.json
4. Use these to contextualize the user's message
5. If a thread match becomes clear → switch to Branch A
6. If genuinely new topic → proceed with MEMORY.md context only, create new thread later
```

### Branch C: Maintenance Session

Triggered when: `memory_review_due` flag is true, or user explicitly asks to
review/organize memory.

```
1. Load MEMORY.md in full (including Fading section)
2. Load last 5 daily logs (headers + decisions sections only)
3. Cross-reference: which MEMORY.md entries were reinforced by recent sessions?
4. Propose promotions, merges, demotions
5. Update maintenance log
```

---

## Phase 4: Deep Recall

**On-demand. Cost: variable (500-3000+ tokens).**

Triggered mid-session when:
- The user references something not in currently loaded context
- A topic resurfaces that was archived
- The agent needs to verify a past decision or its reasoning
- Conflicting information appears and needs resolution

### Retrieval Strategies

**Strategy 1: Targeted Log Lookup**
When: the agent knows approximately *when* something happened.
```
1. Use cross-references from threads.md to identify specific daily logs
2. Load only the relevant section of that daily log (decisions, open questions, etc.)
3. Do NOT load the full log unless the section reference is insufficient
```

**Strategy 2: Index Search**
When: the agent knows *what* but not *when*.
```
1. Read memory/index.md (see Index File spec below)
2. Find entries matching the topic
3. Load the referenced daily log sections
4. If the query is event-sensitive, also scan/rank memory/events.json for direct entity matches and dated event candidates
```

**Strategy 3: Archive Recovery**
When: a topic resurfaces that was previously archived.
```
1. Load memory/archive.md
2. Find the relevant entry
3. Follow its "Key references" to original daily logs if needed
4. If the topic is now active again, promote it back to MEMORY.md > Fading
```

**Strategy 4: Broad Scan (expensive, last resort)**
When: none of the above strategies locate the needed information.
```
1. Load daily log headers (first 5 lines) for the last 30 days
2. Identify candidate logs by header content
3. Load full candidate logs one at a time until found
4. If not found in 30 days, check archive.md
```

---

## Lightweight Deterministic Temporal Support

Use small deterministic helpers only for narrow tasks:
- pairwise ordering ("which happened first")
- date deltas ("how many days/weeks/months between")
- before-threshold counts ("how many X before Y")

Procedure:
1. Retrieve top candidate events from `events.json`
2. Prefer events with `normalized_date`
3. Compute pairwise ordering or deltas in code
4. Feed the computed evidence to the model as structured hints
5. Let the model answer, unless the deterministic mapping is unambiguous and the calling workflow explicitly wants a direct computed answer

Do not over-prune. If the deterministic layer narrows the event set too aggressively, it can regress performance.

## Mid-Session Triggers

The agent should monitor the conversation for signals that deeper retrieval is
needed. These are patterns in the user's messages or the agent's own uncertainty:

| Trigger Signal                                   | Action                           |
|--------------------------------------------------|----------------------------------|
| "Remember when we..." / "We talked about..."     | Phase 4, Strategy 1 or 2        |
| "Didn't we decide..." / "Why did we..."          | Phase 4, Strategy 1 (decisions)  |
| User references a topic not in loaded context     | Phase 4, Strategy 2             |
| Agent is uncertain about a past commitment        | Phase 4, Strategy 1             |
| A closed/archived thread becomes relevant         | Phase 4, Strategy 3             |
| Agent can't find what it needs                    | Phase 4, Strategy 4 (last resort)|

---

## Token Budget Management

The agent should track approximate token usage for memory content and enforce
soft limits to preserve context window space for the actual conversation.

### Budget Allocation (for a ~100k token context window)

```
Memory loading:    5,000 tokens max (5%)    — hard ceiling
  Phase 1-2:         500 tokens             — fixed
  Phase 3:         1,500 tokens             — typical, up to 2,500
  Phase 4:         2,000 tokens             — per retrieval, cumulative cap 3,000
System prompt:    ~2,000 tokens             — fixed
Conversation:    93,000 tokens             — protected, never invaded by memory
```

### When Approaching Budget Limits

1. Summarize loaded daily logs into key points, discard raw content
2. Drop Fading section of MEMORY.md
3. Load only thread headers, not full thread bodies
4. Refuse Phase 4 Strategy 4 (broad scan) — ask the user to help narrow it down

---

## The Index File

When daily logs exceed ~30 files, sequential scanning becomes impractical.
The system generates and maintains an index.

### memory/index.md

```markdown
# Daily Log Index

> Auto-generated. Rebuilt weekly or when daily log count changes by 5+.
> Each entry: date, active threads, key topics, decisions made.

| Date       | Threads Touched   | Key Topics                        | Decisions |
|------------|-------------------|-----------------------------------|-----------|
| 2026-03-22 | wm-design         | schema prototyping, file structure | 3         |
| 2026-03-21 | wm-design         | retrieval workflow, token budgets  | 1         |
| 2026-03-20 | wm-design, ident  | cross-referencing, continuity      | 2         |
| ...        | ...               | ...                               | ...       |
```

### Index Maintenance Rules

- Rebuilt automatically when `daily_log_count % 5 == 0`
- Each row generated by reading the first 10 lines + Decisions section of each log
- Old entries (60+ days) are summarized into monthly rollups
- The index itself should never exceed ~500 tokens

---

## Loading Decision Flowchart

```
SESSION START
│
├─ Read state.json
│  ├─ time_gap < 2h? ──→ Read resumption.md → START CONVERSATION (light)
│  └─ time_gap >= 2h?
│     │
│     ├─ Read resumption.md
│     │
│     ├─ Incoming message matches known thread?
│     │  ├─ YES → Load that thread + relevant MEMORY.md section
│     │  └─ NO  → Load full MEMORY.md + all thread headers
│     │
│     ├─ memory_review_due?
│     │  └─ YES → Queue maintenance (Branch C) after initial response
│     │
│     └─ START CONVERSATION (standard)
│
MID-SESSION
│
├─ User references unknown past event? → Phase 4 retrieval
├─ Agent uncertain about past decision? → Phase 4 retrieval
├─ New ongoing topic emerges? → Create thread stub in threads.md
└─ Token budget approaching limit? → Summarize and compact loaded memory
│
SESSION END
│
├─ Write/append daily log
├─ Update threads (advance position, close if resolved)
├─ Update state.json (timestamp, counters, flags)
├─ Write resumption.md (first-person handoff)
└─ If session_counter.since_last_memory_review >= 5 → set memory_review_due flag
```
