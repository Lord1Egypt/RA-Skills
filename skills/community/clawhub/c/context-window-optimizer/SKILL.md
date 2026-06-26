---
name: context-window-optimizer
description: "Optimize context window usage by summarizing old conversation segments, extracting key facts and decisions to permanent memory, and keeping current context lean. Triggers when: (1) conversation history grows beyond ~50 messages or context feels heavy; (2) before long or complex tasks; (3) after significant decisions or work completions; (4) when explicitly asked to optimize context, compact context, or clean up context."
---

# Context Window Optimizer

Manage context strategically to prevent token waste and keep conversations effective.

## Core Principle

**Context is a shared resource.** Keep it lean so there's room for actual work.

## When to Optimize

- Conversation exceeds ~50 messages
- Context feels heavy before a new task
- Starting a complex multi-step task
- After significant decisions or completions
- Explicit request to optimize/compact

## Optimization Workflow

### Step 1: Assess Context State

Run the analyzer to get context metrics:
```bash
python3 scripts/analyze_context.py --session current
```

This reports:
- Message count and approximate token count
- Age of oldest message
- Density score (signal vs noise)

### Step 2: Identify Optimization Targets

Look for:
- Old已完成 tasks with verbose logs
- Repeated explanations of same concept
- Off-topic tangents
- Raw tool outputs that could be summarized
- Decisions that should move to permanent memory

### Step 3: Extract to Memory

**Decisions → `MEMORY.md` or relevant project file:**
```
## Decisions (from 2026-03-25 session)
- Chose PostgreSQL over MongoDB for project X
- Agreed on 3-day sprint cadence
- User prefers detailed explanations, not summaries
```

**Key facts → appropriate domain/project file:**
```
## Project X Facts
- Tech stack: React + Node + Postgres
- Main user pain point: slow onboarding
- Current velocity: 5 story points/sprint
```

**Patterns → `~/self-improving/memory.md`:**
```
## User Preferences
- Always explain the "why" before the "what"
- Prefers bullet points over paragraphs
```

### Step 4: Summarize Dense Segments

For long work sessions, create a summary instead of keeping all details:

```markdown
## Session Summary: 2026-03-25

### Work Completed
- Set up authentication flow
- Fixed memory leak in worker process
- Designed new API schema

### Decisions Made
- Use JWT over sessions (simpler, scales better)
- Defer caching to v2 (not blocking)

### Open Questions
- Final tech stack for notifications (push vs polling)
- Need user feedback on onboarding flow

### Next Steps
- Implement auth endpoints
- Write tests for worker
- Schedule design review
```

### Step 5: Archive, Don't Delete

Never delete context — archive it:
- Move summaries to `memory/YYYY-MM-DD.md`
- Keep pointers in session for recovery
- Use `[[archived:filename.md]]` notation

## Context Density Rules

| Content Type | Action |
|--------------|--------|
| Completed tasks | Summarize outcome, archive details |
| Decisions | Extract to MEMORY.md or project file |
| Key facts | Extract to relevant domain/project |
| Tool logs | Summarize if successful, keep if debugging |
| Repeated concepts | Remove duplicates, keep one canonical |
| Off-topic | Skip or summarize in notes |
| System prompts | Never touch |
| Skills metadata | Only load relevant ones |

## Quick Commands

| Task | Command |
|------|---------|
| Analyze current context | `python3 scripts/analyze_context.py --session current` |
| Summarize session | `python3 scripts/summarize_session.py --session current --output summary.md` |
| Extract decisions | `python3 scripts/extract_decisions.py --session current` |

## Files

- `scripts/analyze_context.py` — Context metrics and optimization suggestions
- `scripts/summarize_session.py` — Create session summary
- `scripts/extract_decisions.py` — Pull out decisions and key facts
- `references/patterns.md` — Common summarization patterns
