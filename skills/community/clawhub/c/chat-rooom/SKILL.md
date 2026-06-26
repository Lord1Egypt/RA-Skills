---
name: Chat Rooom
slug: chat-rooom
version: 1.0.0
homepage: https://clawic.com/skills/chat-rooom
description: Create local chat rooms for AI agents with channels, mentions, task claims, and durable summaries in the workspace.
changelog: Initial release with a local room protocol, mention routing, claim tracking, and summary driven handoffs.
metadata: {"clawdbot":{"emoji":"💭","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/chat-rooom/"]}}
---

## Setup

If `~/chat-rooom/` does not exist or is empty, read `setup.md` silently. Default to local-first coordination and keep persistence light until the user confirms they want a durable room workflow.

## When to Use

User wants multiple agents to talk, coordinate, debate, or hand off work without copying terminal output around. Use when a task benefits from channels, mentions, lightweight ownership, or an auditable shared log inside the current workspace.

## Architecture

Skill memory lives in `~/chat-rooom/`. Active rooms live in the current workspace at `.chat-rooom/`. See `memory-template.md` for both templates.

```text
~/chat-rooom/
|- memory.md       # Activation defaults and durable preferences
|- rooms.md        # Recent room names, roles, and conventions
`- patterns.md     # Coordination patterns that repeatedly worked well

<workspace>/.chat-rooom/
`- rooms/<room>/
   |- room.md              # Purpose, roster, channels, status
   |- summary.md           # Snapshot, decisions, next actions
   |- jobs.md              # Work items with owner and state
   |- claims.md            # File, task, or test ownership
   |- channels/general.md  # Shared timeline
   |- channels/review.md   # Critique and approval requests
   `- inbox/<agent>.md     # Pending mentions and directed asks
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup process | `setup.md` |
| Memory template | `memory-template.md` |
| Room protocol | `protocol.md` |
| Daily operations | `operations.md` |
| Example room patterns | `patterns.md` |

## Core Rules

### 1. Start Coordination Inside a Named Room
- Create or join one named room before multi-agent work starts.
- Keep one room per objective, incident, or milestone so decisions stay discoverable.
- Do not scatter the same coordination across scratch files, comments, and terminal notes.

### 2. Make Every Message Addressable
- Each message should carry one primary intent: ask, update, proposal, decision, block, or handoff.
- Use `@agent` mentions for directed work. Use `@all` only for blocking context changes or final checkpoints.
- Link exact paths, commands, or commits instead of pasting large blobs that bury the action item.

### 3. Claim Shared Surfaces Before Editing Them
- Update the claims table before touching the same file, test target, or subtask as another agent.
- Claim the smallest useful surface to reduce idle waiting.
- Refresh or release stale claims when work is done, blocked, or handed off.

### 4. Read the Summary First and Repair It Often
- On join, read the room summary before scrolling the whole channel history.
- When a thread pauses, update summary with status, decisions, open questions, and next owner.
- If summary and channel history diverge, trust the newer timestamp and fix the summary immediately.

### 5. Separate Channels by Intent
- Keep `general` for status, `review` for critique, `build` for execution details, and `incident` for live recovery.
- Create a new channel when one topic would bury another.
- Once a task becomes active, avoid mixing debate and execution in the same channel.

### 6. Keep the Room Local and Auditable
- Prefer workspace files and local tools over a hosted chat backend unless the user explicitly asks for one.
- Treat the room as an operational log, not as private memory.
- Never store secrets, tokens, or unrelated personal data in room files.

## Common Traps

- Starting a room without a clear objective or roster -> duplicate work and vague ownership.
- Posting long monologues instead of targeted asks -> agents miss the real action item.
- Editing shared files without a claim -> merge collisions and silent overwrites.
- Leaving a room without updating summary or jobs -> the next agent rereads everything.
- Using `@all` for routine chatter -> noisy wakeups and wasted context.

## Security & Privacy

**Data that leaves your machine:**
- None from this skill itself

**Data that stays local:**
- Room logs and defaults in `~/chat-rooom/` and `.chat-rooom/` inside the active workspace

**This skill does NOT:**
- Require a hosted backend
- Access undeclared folders outside the active workspace and `~/chat-rooom/`
- Store credentials or secrets in room logs

## Scope

This skill ONLY:
- Sets up local chatroom coordination patterns for multiple agents
- Keeps channels, claims, jobs, and summaries consistent
- Helps agents talk through room files instead of terminal copy-paste

This skill NEVER:
- Promise real-time transport that is not available locally
- Replace version control or formal code review
- Treat room logs as a secret store

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `chat` - Communication preference memory for cleaner agent interactions.
- `agent` - Agent behavior and prompting patterns for consistent roles.
- `agents` - Multi-agent system design and safety boundaries.
- `agentic-engineering` - Multi-agent operating patterns and coordination strategy.
- `delegate` - Structured handoffs when work should move between agents.

## Feedback

- If useful: `clawhub star chat-rooom`
- Stay updated: `clawhub sync`
