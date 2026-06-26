# File Management Reference

_This is the actual file management system used in production. Adapt to your own setup._

---

## Current Workspace Structure

```
~/.openclaw/workspace/
├── AGENTS.md          # Agent configuration and personality
├── MEMORY.md          # Long-term curated memory (loaded in main session only)
├── DREAMS.md          # Background/ dreaming notes
├── SOUL.md            # Agent persona and tone guidelines
├── USER.md            # User profile and preferences
├── TOOLS.md           # Local tool-specific notes
├── HEARTBEAT.md       # Heartbeat configuration
│
├── memory/            # Daily session logs
│   ├── YYYY-MM-DD.md  # Daily notes (canonical format)
│   ├── dreaming/       # Dream state processing
│   └── archives/      # Old memory archives
│
├── skills/            # Skill directories
│   └── [skill-name]/  # Individual skills
│
├── [project-dirs]/    # Project-specific directories
│
├── api/               # API-related files
├── data/              # Data files
├── public/            # Public assets
├── scripts/           # Utility scripts
├── state/             # State files
└── [*.md]            # Reference docs (strategies, notes)
```

---

## File Categories

### Bootstrap Files (Read-Only)
These define the agent and should rarely change:
- `AGENTS.md` - Workspace instructions
- `SOUL.md` - Persona definition
- `USER.md` - User profile
- `MEMORY.md` - Long-term memory
- `TOOLS.md` - Tool notes
- `IDENTITY.md` - Agent identity
- `DREAMS.md` - Background processing
- `HEARTBEAT.md` - Periodic task config

### Active Reference Files
Currently in use by agents or systems:
- Strategy documents (e.g., `gunner-strategy.md`)
- Project documentation (e.g., `truckpedia-*.md`)
- Team documentation (e.g., `deckhand-tasks.md`)

### Scripts & Executables
- End with `.sh` (bash), `.py` (Python), `.js` (JavaScript)
- Must have executable bit (`chmod +x`) to run via cron
- Location: `~/scripts/` for system crons, workspace for agent-specific

### Logs
- End with `.log`
- Written to by cron jobs and scripts
- Should be gitignored (contain sensitive data sometimes)

---

## Dead File Detection

A file is dead if:

1. **No active cron references it**
   ```bash
   crontab -l | grep filename
   openclaw cron list | grep filename
   ```

2. **No script references it**
   ```bash
   grep -r "filename" ~/scripts/ --include="*.sh"
   grep -r "filename" ~/.openclaw/workspace/ --include="*.sh" --include="*.py"
   ```

3. **Not loaded by any skill or agent**
   ```bash
   grep -r "filename" ~/.openclaw/skills/
   grep -r "filename" ~/.openclaw/agents/
   ```

4. **No recent meaningful modification** (older than 30+ days and obvious stale content)

---

## Cleanup Checklist

Before deleting any file:

- [ ] Check if referenced by any cron job
- [ ] Check if referenced by any script
- [ ] Check if loaded by any skill
- [ ] Check git history for recent changes (may indicate active use)
- [ ] Document what the file did (in case of rollback need)
- [ ] Create git commit with message describing removal
- [ ] Use `trash` not `rm` (recoverable)

---

## Directory Conventions

### memory/
Daily session logs and working context.

- `YYYY-MM-DD.md` - One file per day (canonical)
- `dreaming/` - Background processing notes
- `archives/` - Old memory tarballs

### skills/
Installed skills following OpenClaw skill structure.

- Each skill in its own directory
- `SKILL.md` in each skill root
- Community skills in `~/.openclaw/skills/`

### scripts/
System-level scripts referenced by crontab.

- Typically bash scripts
- Must be executable
- Referenced by system crons in `/etc/crontab` or user crontab

### project-dirs/
Project-specific directories.

- Named after the project
- Contain project-specific files, scripts, configs
- Each project gets its own directory

---

## Naming Standards

| Type | Extension | Example |
|------|-----------|---------|
| Daily memory | `YYYY-MM-DD.md` | `memory/2026-04-27.md` |
| Strategy | `*-strategy.md` | `gunner-strategy.md` |
| Project plan | `*-plan.md` | `truckpedia-plan.md` |
| Notes | `*.md` | `deckhand-tasks.md` |
| Scripts | `.sh`, `.py`, `.js` | `truck-expansion.sh` |
| Logs | `.log` | `cron-output.log` |
| Configs | `.json`, `.yaml` | `systems.json` |

---

## Git Practices

### Before Cleanup
```bash
git add -A
git commit -m "Cleanup: Remove dead files"
git push
```

### Create Revert Point
```bash
git add -A
git commit -m "SAVEPOINT: Before major changes"
```

### Restore if Needed
```bash
git checkout <commit-hash> -- <filename>
```

---

## Common Pitfalls

1. **Deleting too aggressively** — Always verify, use trash
2. **Not documenting** — Note what files did before deleting
3. **No backup point** — Commit before major changes
4. **Inconsistent naming** — Follow the conventions above
5. **Ignoring logs** — Keep logs gitignored, they're not for versioning

---

## When to Audit

- Monthly scheduled review
- After major project completion
- When workspace feels cluttered
- Before major restructuring
- After system/agent issues

---

_This document reflects actual production practices. Update as your setup evolves._
