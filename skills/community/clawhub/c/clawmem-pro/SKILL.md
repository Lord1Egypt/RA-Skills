---
name: openclaw-memory-system
description: "Use whenever the user wants persistent memory across OpenClaw sessions, mentions MEMORY.md, daily notes, cron inbox, heartbeat routines, agent identity, or 'my agent forgot everything.' Also trigger when setting up a new agent workspace, configuring memory extraction crons, or any time the user asks how to make their agent remember things between runs."
---

# OpenClaw Memory System

## What This Skill Does

Implements a complete file-based memory architecture that persists across OpenClaw sessions. Agents wake up with full context instead of starting from zero.

## When to Trigger

- User says "my agent forgets everything"
- User wants to set up memory for their agent
- User mentions MEMORY.md, daily notes, cron inbox, or heartbeat routines
- User asks how to make agent remember between sessions
- Setting up a new agent workspace
- Configuring cron jobs for memory extraction

## Installation (Agent Instructions)

When this skill triggers, the agent should:

1. **Run the installer script** from the skill directory:
   - Windows: `./scripts/install.ps1 -WorkspacePath <workspace>`
   - Linux/macOS: `./scripts/install.sh -WorkspacePath <workspace>`
   - The installer creates: `MEMORY.md`, `HEARTBEAT.md`, `memory/` directory, templates, cron configs

2. **Verify installation** by checking these files exist:
   - `MEMORY.md` — curated long-term memory
   - `HEARTBEAT.md` — periodic check routines
   - `memory/cron-inbox.md` — cross-session message bus
   - `memory/heartbeat-state.json` — state tracking
   - `memory/YYYY-MM-DD.md` — today's daily notes

3. **Seed MEMORY.md** with operator context:
   - Operator name, timezone, communication preferences
   - Active projects, priorities, decisions
   - Important people, relationships, boundaries
   - Tool preferences, coding style, review rules

4. **Configure cron jobs** (optional but recommended):
   - Nightly memory extraction: 23:00 daily
   - Heartbeat check: every 30 minutes
   - Use `./scripts/setup-cron.ps1` or `./scripts/setup-cron.sh`

## Directory Structure After Install

```
workspace/
|-- MEMORY.md                 # Curated long-term memory
|-- HEARTBEAT.md              # Periodic check routines
|-- memory/
|   |-- YYYY-MM-DD.md         # Daily raw logs
|   |-- cron-inbox.md         # Cross-session messages
|   |-- heartbeat-state.json  # Timestamps
|   |-- diary/                # Personal reflections
|   |-- platform-posts.md     # External post tracking
|   └── strategy-notes.md     # Adaptive playbook
```

## Daily Workflow

### On Every Session Start
1. Read `MEMORY.md` — who you are, operator context, priorities
2. Read `memory/YYYY-MM-DD.md` (today + yesterday) — recent context
3. Check `memory/cron-inbox.md` — messages from other sessions

### During the Session
4. Write everything significant to `memory/YYYY-MM-DD.md`:
   - Decisions made, lessons learned
   - Errors encountered and how fixed
   - New projects started, completed milestones
   - Changes to operator preferences or context
   - Format: `## HH:MM -- Brief title`
   - Be raw and verbose — this is working memory

### Before Session Ends
5. Check if cron inbox needs processing
6. If significant events occurred, append a summary to MEMORY.md under relevant sections

## Heartbeat Routine

The heartbeat script (`scripts/heartbeat-check.ps1` or `.sh`) runs periodically and:
1. Processes `memory/cron-inbox.md` entries into daily notes
2. Clears the inbox after processing
3. Updates `memory/heartbeat-state.json` with timestamps
4. Checks for stale or completed cron jobs

## Memory Extraction

The nightly cron (`scripts/memory-extract.ps1` or `.sh`) at 23:00:
1. Reads today's daily notes
2. Looks for significant keywords: decided, lesson, milestone, completed, shipped, fixed, breakthrough
3. Extracts matching entries with context
4. Appends to `MEMORY.md` under a dated "Daily Extracts" section
5. Marks daily notes as extracted

## Writing Good Daily Notes

- Timestamp every entry: `## HH:MM -- What happened`
- Include context: what triggered it, what was decided, rationale
- Don't censor — this is raw working memory, not curated wisdom
- Significant entries will be extracted automatically
- Review MEMORY.md weekly to remove outdated info

## Security Rules

- `MEMORY.md` may contain operator-specific info — only load in trusted (direct) sessions
- Skip MEMORY.md in group chats or shared contexts
- Never share operator personal details externally without approval
- Keep private info private

## Customization

### Adjust Extraction Keywords
Edit `scripts/memory-extract.ps1` (or `.sh`) `$significanceKeywords` array:
- Default: decided, lesson learned, important, breakthrough, milestone, completed, shipped, fixed
- Add domain-specific keywords as needed

### Add New Heartbeat Checks
Edit `HEARTBEAT.md` and `scripts/heartbeat-check.*` to add custom periodic checks:
- Service health checks
- File cleanup routines
- External API status checks

### Change Cron Schedule
Edit `scripts/setup-cron.ps1` or `scripts/setup-cron.sh`:
- Memory extraction: default 23:00
- Heartbeat: default every 30 min
- Daily notes reminder: default 09:00

## Troubleshooting

**Agent still forgets between sessions:**
- Verify AGENTS.md includes "Read MEMORY.md on every session"
- Check that MEMORY.md file exists and is readable
- Ensure daily notes are being written

**Cron inbox not processing:**
- Check heartbeat-state.json for last run timestamp
- Verify cron jobs are scheduled (run `./scripts/setup-cron.*`)
- Check if heartbeat-check script exists and is executable

**Memory extraction not running:**
- Verify cron job is scheduled
- Check that daily notes exist for extraction
- Review extraction keywords if nothing is being picked up

## Templates

All templates live in `templates/`:
- `MEMORY.md` — Long-term memory structure
- `HEARTBEAT.md` — Periodic routines
- `daily-notes.md` — Daily log format
- `cron-inbox.md` — Cross-session message format
- `heartbeat-state.json` — State tracking JSON
- `platform-posts.md` — External post tracking
- `strategy-notes.md` — Adaptive playbook

Copy these during installation; do not modify originals.

## Cross-Platform

Scripts provided for both PowerShell (Windows) and Bash (Linux/macOS):
- `*.ps1` — PowerShell scripts
- `*.sh` — Bash scripts

Always check both versions exist when editing.

## Scripts Reference

| Script | Purpose |
|---|---|
| `install.ps1` / `install.sh` | One-command setup |
| `setup-cron.ps1` / `setup-cron.sh` | Configure automated cron jobs |
| `memory-extract.ps1` / `memory-extract.sh` | Nightly extraction from daily notes |
| `heartbeat-check.ps1` / `heartbeat-check.sh` | Periodic inbox processing |

All scripts support `-WorkspacePath` for custom directories and `-DryRun` for preview.
