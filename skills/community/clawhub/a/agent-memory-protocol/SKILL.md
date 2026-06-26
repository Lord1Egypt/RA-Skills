---
name: memory-manager
description: Agent memory management protocol. Activate for any memory read, write, or update operation. Defines six-category write spec, L0 sync rules, and dedup strategy.
triggers:
  - memory management
  - remember this
  - update memory
  - memory write
  - flush memory
---

# Memory Manager Skill

> ⚠️ **All-Agent Protocol**: This protocol applies to all agents in the system.
> Any agent completing a subtask that produces persistable information must write it according to this spec. Do not create memory files outside this structure.

---

## When to Trigger
- Before a conversation ends and new information needs storing
- When the user says "remember", "update memory", or similar
- When existing memory needs correction
- After completing a new type of task (new case)
- **Real-time trigger during conversation**:
  - Project deadline changes → immediately update `blackboard/projects/<id>.md` + `blackboard/REGISTRY.md` (SSOT)
  - Progress milestone completed → immediately update the corresponding Blackboard project card
  - Habit / preference changes → immediately update preferences/
  - Person / tool info changes → immediately update entities/
  - No need to wait for end of conversation or explicit instruction

---

## Three-Layer Density Structure

| Layer | File | Purpose | Update Frequency |
|-------|------|---------|-----------------|
| **L0** | `MEMORY.md` | Minimal index, 1-3 sentences per category + path pointers | Only on structural changes |
| **L1** | `memory/INDEX.md` | Category overview navigation, ~500-1000 words | When L2 file structure changes |
| **L2** | `memory/user/` `memory/agent/` | Full details, read on demand | Day-to-day maintenance |

**Retrieval order**: Read L0 (MEMORY.md) to locate category → memory_get the relevant L2 → use memory_search for full-text search when uncertain.

---

## Directory Structure (L2)

```
memory/
├── INDEX.md                    ← L1 navigation
├── user/
│   ├── profile.md              # Basic info (appendable)
│   ├── preferences/            # Preferences (appendable)
│   │   ├── learning.md
│   │   ├── lifestyle.md
│   │   ├── tech.md
│   │   └── communication.md
│   ├── entities/               # Entities (updatable)
│   │   ├── tools.md
│   │   └── people.md
│   └── events/                 # Events (append-only)
│       └── YYYY-MM-event-name.md
└── agent/
    ├── cases/                  # Cases (append-only)
    │   └── case-name.md
    └── patterns/               # Patterns (appendable)
        ├── task-delegation.md
        ├── config-backup.md
        └── memory-write.md
```

---

## Classification Decision Flow

```
New information → determine type
  ├── User identity/background/data change → user/profile.md
  ├── User preferences/habits/style → user/preferences/[topic].md
  ├── Project/tool/person info → user/entities/[type].md
  ├── Key decisions/milestones/irreversible events → user/events/YYYY-MM-[name].md (new file)
  ├── First time handling a new task type → agent/cases/[name].md (new file)
  └── Reusable processing pattern discovered → agent/patterns/[name].md
```

---

## Write Specification

### Format Standards
- Each file has `# Title` + structured content
- Appended content is date-stamped: `_Updated: YYYY-MM-DD_`
- No stream-of-consciousness; write conclusions only

### Integration Pattern for New Knowledge / Rules / Skills

When receiving new knowledge, rules, or a skill, **do not just stack it on top** — follow this flow:

```
1. Search for existing similar content (memory_search / read relevant skill or pattern files)
2. Compare differences, derive the better conclusion (dedup, absorb, correct)
3. Update the complete content in the authoritative source file
4. Other files referencing that content become pointer-style, not independently maintained
```

> Store details in one place only. Other files use "see X" pointers to avoid future drift.

See `memory/agent/patterns/memory-write.md` → "Integration pattern for new knowledge/rules"

---

### Cascade Update Rules (Mandatory)

Any change involving the following must check and sync all referencing L1/L2 source files after writing today's memory:

- Agent config / model assignment
- Toolchain / channel changes
- Project status / deadlines
- Protocol rule changes

**How**: When unsure which files are affected, use `memory_search` on keywords and verify each one.
Today's event log (`memory/YYYY-MM-DD.md`) cannot replace source file updates — it is a log, not the source of truth.

---

### Dedup Strategy
| Situation | Action |
|-----------|--------|
| Exact duplicate of existing | Skip, do not write |
| Update to existing info | Append to end of file with date stamp |
| Conflicts with existing | Add "updated" note after existing entry, append new version |
| Entirely new info | Create new file or append to appropriate category |
| events / cases | Always create new file, never modify existing |

### Prohibited Actions
- ⚠️ The `memory/` root dir may hold current-week session logs (≤7 days); crontab auto-archives to `memory/archive/YYYY-MM/` on the 1st of each month. Non-log files (profile/preferences/entities/events/cases/patterns) must go in their L2 category directories
- ❌ Do not write stream-of-consciousness directly to MEMORY.md
- ❌ Do not modify existing files under events/ or cases/

---

## L0 Sync Rules (MEMORY.md)

MEMORY.md is the L0 index; keep it under 30 lines.

**When to update MEMORY.md:**
1. New events or cases file added → add a one-line pointer in the relevant block
2. Key patterns have major changes → update the summary sentence
3. User basic info has major changes → update the user block

**When MEMORY.md does not need updating:**
- Small amount of info appended to an existing file
- Routine entities data updates (project progress, etc.)

**L0 summary format:**
```markdown
- **[keyword]**: [one-sentence summary] → `memory/path`
```

---

## L1 Sync Rules (memory/INDEX.md)

**When to update INDEX.md:**
1. New L2 file added (new case / event / pattern) → add a row in the corresponding table
2. A file's topic has major changes → update the corresponding summary column
3. Old-format file officially migrated → remove from "to-migrate" list

---

## Topic Archive & Compression Protocol

### When to Trigger Archival
| Trigger | Action |
|---------|--------|
| User says "done / finished / next" | Immediately generate topic summary, write to appropriate category |
| Conversation > 30 turns / tool calls > 40 | Compress closed topics, free context |
| New session starts (/new triggered) | Archive previous session's open items to corresponding Blackboard project card |

### Compression Summary Format (3-line principle)
Write completed topics in the following format — **do not retain raw conversation**:

```markdown
## [YYYY-MM-DD] Topic Title
Status: ✅ Done / 🔄 In Progress / ⏸️ Pending
Key points: [1-2 sentences of core content or decision]
Decision: [key decision, omit if none]
Follow-up: [only incomplete items; omit if done]
→ Details: [path to detail file if any, otherwise omit]
```

### Tiered Storage Rules
- **Completed topics** → write summary (3-5 lines) + `status: done`, do not retain details
- **In-progress tasks** → update `blackboard/projects/<id>.md` + one-line progress in `blackboard/REGISTRY.md`
- **Key decisions / irreversible events** → write to `memory/user/events/` (permanent)
- **Reusable patterns** → write to `memory/agent/patterns/` (permanent)

### Session Reflection

At session end (/new, idle reset, or user actively switches), if the session contained any of the following, **extract one pattern**:

| Trigger | Reflection content | Write to |
|---------|-------------------|----------|
| User corrected a behavior | "Next time X occurs, do Y" | `memory/agent/patterns/` or `.learnings/` |
| A plan failed and was replaced | "Plan X failed because A; switched to Y" | `memory/agent/patterns/` |
| Discovered a hidden tool/config gotcha | "When using X, watch out for Y" | `memory/agent/patterns/` or TOOLS.md |
| Found a better approach than what docs say | "Better approach for X is Y" | `memory/agent/patterns/` |

**Format**:
```markdown
## [YYYY-MM-DD] Title
- **Trigger**: what situation was encountered
- **Lesson**: one-sentence conclusion
- **Next time**: specific action guidance
```

**When reflection is NOT needed**: pure execution tasks, no corrections, no surprises, routine CRUD.

**Relationship to Instinct**: Reflection written to patterns/ is low-barrier recording. When the same entry is triggered ≥3 times, promote to a YAML instinct in `.learnings/instincts/` (see AGENTS.md §4).

---

## Context Pressure Management (Memory Flush Protocol)

Run `session_status` to monitor context usage; proactively write to memory at these thresholds:

| Context % | Action |
|-----------|--------|
| < 50% | Normal operation, write on decision |
| 50–70% | Alert state, write key points after each important exchange |
| 70–85% | Active flush, immediately write important content to memory |
| > 85% | Emergency flush, stop and write a full context summary before continuing |

**Must-flush content**: decisions made and rationale, pending items and owners, unresolved problem threads.

### Flush Checklist (check each item to prevent omissions)

At session end, before compaction, or when user says "done / next" — **scan each item**:

| # | Check | Write target | Trigger words |
|---|-------|-------------|---------------|
| 1 | User preference changed? (taste/habit/tool choice) | `memory/user/preferences/` | "I prefer…" "stop doing…" "switch to…" |
| 2 | Project progress advanced? | `blackboard/projects/<id>.md` + REGISTRY | done/blocked/delayed/milestone |
| 3 | New decision made? | Project card "conclusions" or `memory/user/events/` | "decided…" "confirmed…" "not doing" |
| 4 | Person/entity info updated? | `memory/user/entities/` | new contact / tool change / account info |
| 5 | Reusable pattern discovered? | `memory/agent/patterns/` | gotcha / detour / better solution |
| 6 | User corrected something? | `.learnings/LEARNINGS.md` | explicit correction / dissatisfied / redo |

**How**: Don't need all to fire. Scan the conversation quickly, write what hit, skip what didn't. Takes 3 seconds — don't skip it.

---

## Sub-Agent Write Rules

When any sub-agent completes a task with persistable information:
1. **Blackboard project state**: update project card + corresponding REGISTRY row directly (spec → `blackboard/_schema.md`). No need for grep-level cascade checks; the orchestrating agent handles that.
2. **Memory-type info**: write to the appropriate L2 file per this protocol, note `_Written by: [agent name] YYYY-MM-DD_` at the end
3. Notify the orchestrating agent after writing; it syncs L0/L1 indexes as needed
