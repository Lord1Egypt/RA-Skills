# Memory Template - Auto-Update

Create `~/auto-update/memory.md` with this structure:

```markdown
# Auto-Update Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Context
- What the user wants updated automatically
- Whether this should activate on install-time conversations

## Defaults
- New skill default: all-in | all-out
- OpenClaw mode: auto | notify | manual
- Summary style: terse | standard | deep

## Boundaries
- Changes that always require approval
- Backup depth the user is comfortable with
- Whether migration risk always pauses skill updates

## Notes
- Lessons learned from recent update runs

---
*Updated: YYYY-MM-DD*
```

Create `~/auto-update/openclaw.md` with this structure:

```markdown
# OpenClaw Policy

## Install State
- Install method:
- Channel:
- Current version:

## Core Update Behavior
- Preferred update path:
- Auto-update enabled or not:
- Dry-run before apply:

## Backup Scope
- Always snapshot:
- Optional snapshot:

## Post-Update Review
- Tailored feature review: yes | no
- Notify where:
```

Create `~/auto-update/skills.md` with this structure:

```markdown
# Skill Update Ledger

## Defaults
- New skills inherit: all-in | all-out

## Tracked Skills
- slug:
  location:
  installed_version:
  auto_update: yes | no | inherit
  last_backup:
  migration_state: clean | pending | ask-first
```

Create `~/auto-update/schedule.md` with this structure:

```markdown
# Update Schedule

## Timing
- Timezone:
- Discovery cadence:
- Apply cadence:
- Quiet hours:

## Ownership
- Scheduler type:
- Who may edit it:
- No-op behavior:
```

Create `~/auto-update/backups.md` with this structure:

```markdown
# Backup Inventory

## OpenClaw
- Date:
  version:
  files:
  path:

## Skills
- slug:
  date:
  version:
  path:
```

Create `~/auto-update/migrations.md` with this structure:

```markdown
# Migration Queue

## Pending
- slug:
  from_version:
  to_version:
  possible_changes:
  user_decision:

## Cleared
- YYYY-MM-DD - slug - short note
```

Create `~/auto-update/run-log.md` with this structure:

```markdown
# Run Log

## YYYY-MM-DD HH:MM
- Trigger:
- OpenClaw:
- Skills:
- Backups:
- Migrations:
- Verification:
- Next action:
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Defaults are still being tuned | Keep asking only for missing high-value decisions |
| `complete` | Stable update policy exists | Reuse defaults and ask only on exceptions |
| `paused` | User wants manual control for now | Do not push automation changes |
| `never_ask` | User does not want further calibration | Act only on direct requests |

## Key Principles

- The global default decides how new skills start, not how every skill must stay forever.
- Backups and migration notes are part of the updater, not optional extras.
- Keep the ledgers compact enough to scan before any update run.
