---
name: agent-essentials
description: Meta-skill for capability expansion and cautious self-improvement. USE WHEN (a) a request suggests a missing capability, external platform support, workflow automation, integration work, or any reusable process that may benefit from skill discovery before giving up — common phrases include "automate X", "integrate with X", "support X platform", "帮我自动化X", "对接X", "做一个工具来X"; OR (b) a meaningful failure, user correction, recurring mistake ("again", "this is the Nth time", "又错了", "这是第N次了"), or better workflow should be captured and routed into a durable file (AGENTS.md / TOOLS.md / USER.md / SOUL.md). DO NOT use for one-off questions or trivial noise.
---

# Agent Essentials

This skill has two jobs:

1. **Expand capabilities** — discover better capability paths before declaring failure.
2. **Self-improve** — capture important lessons and route them to the right durable layer.

## Capability Expansion

**Rule**: never stop at "I can't" or "no built-in way" without checking for a better capability path.

**Triggers** — request implies external platform / workflow automation / system integration / repeatable ops / capability gap. Common phrasing: *"automate X" / "integrate with X" / "support X platform" / "help me do this in X"*.

### Workflow

1. **Detect the gap**
   - **Input**: the user's request.
   - **Test**: would solving this same request appear ≥2 times across this user's work? OR does it require a tool/platform not in the loaded skill list?
   - **Output**: a 1-line verdict — `gap: <yes/no> — <which capability is missing>`. If `no`, exit this workflow and answer normally.
   - **If ambiguous**: count yes on {*reusable later? / specific platform? / >1 step?*}; ≥2 yes → treat as gap.

2. **Search**
   - **Input**: gap verdict + missing-capability keywords from step 1.
   - **Where**: (a) loaded skill list — match name/description/triggers; (b) ClawHub via `https://clawhub.ai/search?q=<keyword>`, try 1–3 variants.
   - **Stop**: strong match found OR 3 variants returned nothing.
   - **Output**: 1–3 candidates as `<name> — <one-line value> — <fit: strong/moderate/weak>`.

3. **Act** — pause for user confirmation before any of these:
   - **Installing a skill** → show name, source, one-line value, and ask "install? [y/N]" before downloading.
   - **Creating a new custom skill** → show the proposed name + 3-line description and ask before scaffolding.
   - **Doing the task directly** → only this branch may proceed without confirmation, and only if no fallback above is viable.

## Self-Improvement

**Rule**: when something meaningful is learned, preserve the minimum useful lesson.

**Triggers** — meaningful failure / user correction / recurring mistake / discovery of a better workflow. Do **not** log trivial failures or one-off noise.

### Workflow

1. **Capture**
   - **Input**: the trigger event (failure / correction / insight).
   - **Output**: a 3-line lesson:
     ```
     What: <what went wrong or was discovered>
     Correct: <the actually correct behavior>
     Next time: <concrete trigger → action>
     ```
   - **Reject**: can't fit in 3 lines → lesson too vague, sharpen first.

2. **Route**
   - Store the learning in the right place:

| Type | Destination | Confirm? |
|---|---|---|
| Session note | Daily memory / learnings file | — |
| Workflow rule | `AGENTS.md` | ✓ |
| Tool gotcha | `TOOLS.md` | ✓ |
| Voice / boundary pattern | `SOUL.md` | ✓ |
| User preference | `USER.md` or long-term memory | ✓ |
| Missing capability | Skill discovery (see above) | ✓ |

   - For any ✓ row: show the diff and ask "append to <file>? [y/N]" before writing. Never silently mutate durable files.

3. **Promote** to durable file only if **all** hold:
     - **Recurring** — ≥2 occurrences (user saying "Nth time" / "又错了" is proof)
     - **High-value** — non-trivial consequence (broken CI, lost work, wrong user output), not style nits
     - **Broadly reusable** — class of situations, not one specific file/PR
     - **Rule-preventable** — a future-you reading the rule would avoid it
   - If any fails, keep in daily memory only.

## File Locations

Resolve durable files in this order — first hit wins:

| File | Lookup order |
|---|---|
| `AGENTS.md` | `./AGENTS.md` → `~/.claude/AGENTS.md` |
| `TOOLS.md` | `./TOOLS.md` → `~/.claude/TOOLS.md` |
| `SOUL.md` | `./SOUL.md` → `~/.claude/SOUL.md` |
| `USER.md` | `~/.claude/USER.md` (always user-scoped) |
| Daily memory | `~/.claude/memory/YYYY-MM-DD.md` (auto-create if missing) |

If none exists and a write is approved, create at the project-root path (or `~/.claude/` for `USER.md`) and tell the user "creating new file `<path>`."

## Decision Tree

```text
Something notable happened
├─ Capability gap?
│  └─ Search → Recommend → Install or fallback
├─ Lesson worth keeping?
│  └─ Capture → Route → Promote if recurring
└─ Neither
   └─ Continue normally
```

## Edge Cases

- **User declines install** → fall to "do directly" or "create custom"; do not re-pitch in this session.
- **ClawHub unreachable** → state failure; rely on local list only; offer retry.
- **2+ candidates tie "strong"** → show all + 1-line differentiator and let user pick; never silently choose.

## Principles

- Search before saying "nothing exists." Prefer short learnings over elaborate templates.
- Do not promote one-off lessons. Do not install weak-matching skills just to reduce uncertainty. Do not rewrite major workspace files casually.
