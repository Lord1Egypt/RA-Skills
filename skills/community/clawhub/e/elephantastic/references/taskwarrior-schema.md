---
version: 1.0.0
last_updated: 2026-03-28
---

# Taskwarrior Schema Reference

## Installation

```bash
# Debian/Ubuntu
sudo apt install taskwarrior

# macOS
brew install task

# Arch
sudo pacman -S task
```

## Recommended `.taskrc`

```ini
# Core
data.location=~/.task
default.command=next

# Context: what the agent can actually do
context.main.read=@computer or @online or @agent
context.main.write=

# UDAs
uda.brainpower.type=string
uda.brainpower.label=Brainpower
uda.brainpower.values=H,M,L
uda.estimate.type=numeric
uda.estimate.label=Estimate (min)

# Urgency weights
urgency.user.tag.in.coefficient=15.0
urgency.user.tag.next.coefficient=12.0
urgency.user.tag.gate.coefficient=-10.0
urgency.user.tag.waiting.coefficient=-5.0

# Reports
report.in.description=Inbox (unprocessed)
report.in.columns=id,description,project,tags,entry.age
report.in.filter=status:pending +in
report.in.sort=entry-
```

## Core Commands

```bash
# Add
task add "description"
task add project:Goals +next priority:H "strategic goal"

# View
task next                          # default: actionable, sorted by urgency
task list                          # all pending
task project:Internal list         # filter by project
task +error list                   # filter by tag
task +in list                      # inbox

# Modify
task <id> modify priority:H
task <id> modify project:Internal.Ops
task <id> modify +next -in
task <id> modify wait:2025-02-28

# Annotate
task annotate <id> "note or context"

# Complete
task done <id>

# Delete
task delete <id>

# Projects
task projects
task project:Internal.Learnings list

# Burndown
task burndown.daily
task +growth burndown.daily
```

## Tag Taxonomy

### GTD Tags
| Tag | Meaning |
|---|---|
| `+in` | Inbox — not yet triaged |
| `+next` | Selected for action |
| `+waiting` | Blocked on external |
| `+tickle` | Snoozed, will resurface |
| `+gate` | Requires human approval before completion |

### Learning Tags
| Tag | Meaning |
|---|---|
| `+error` | Command / tool failure |
| `+learning` | User correction or knowledge gap |
| `+featreq` | Missing capability |
| `+promoted` | Elevated to SOUL.md / AGENTS.md / TOOLS.md |

### Work Tags
| Tag | Meaning |
|---|---|
| `+growth` | Self-improvement or toolsmithing |
| `+rnd` | Research task (assumes `@computer @online`) |
| `+rnr` | Read and review — annotate the task with the URL |
| `+toolsmith` | Tool creation / improvement |
| `+drift` | Identity or behavioral drift correction |
| `+think` | Deferred decision — must decide immediately when it resurfaces (no re-snooze) |
| `+tickle` | Snoozed item — hidden until `wait:` date |

### Context Tags
| Tag | Meaning |
|---|---|
| `@computer` | Needs local execution |
| `@online` | Needs network access |
| `@agent` | Fully autonomous, agent can self-execute |
| `@phone` | Human action required on mobile |

## Custom Report: Learnings

Add to `.taskrc`:
```ini
report.learnings.description=Error & Learning Log
report.learnings.columns=id,tags,priority,description,entry.age
report.learnings.filter=project:Internal.Learnings status:pending
report.learnings.sort=entry-
```

Usage: `task learnings`

## Recurrence Counting Pattern

When the same error occurs again:
1. `grep` existing tasks for the pattern: `task +error list | grep "keyword"`
2. If found: `task annotate <id> "recurrence #2 — [date]"`
3. At recurrence #3 within 30 days → promote the fix

## Integration with Session State

On session start:
```bash
task active     # any tasks marked started?
task next       # what should I pick up?
```

On session end:
```bash
task stop <id>  # stop active time tracking (if using timewarrior)
# write ops/session_state.md with current task id and last action
```

## Timewarrior Integration (optional)

If `timew` is installed, Taskwarrior hooks auto-track time:
```bash
task start <id>   # begins time tracking
task stop <id>    # ends interval
timew summary     # see where time went
```
