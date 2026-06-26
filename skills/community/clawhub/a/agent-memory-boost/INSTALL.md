# Install

## Prerequisites

- OpenClaw installed and running
- Python 3 (only needed if OpenClaw CLI is unavailable)

## Option 1: ClawHub

```bash
npx clawhub@latest install memory-boost
```

Then run the setup script to create the memory directory and cron jobs:
```bash
cd ~/.openclaw/skills/memory-boost
./install.sh
```

## Option 2: Git clone + install script

```bash
git clone https://github.com/TechieTer/openclaw-memory-boost.git
cd openclaw-memory-boost
./install.sh
```

No arguments needed. The script:
1. Installs the skill to `~/.openclaw/skills/memory-boost/`
2. Creates `~/.openclaw/memory/` with the template, task index, and loop state marker
3. Adds all 5 cron jobs (uses `openclaw cron add` if available, otherwise merges into `jobs.json`)

Options:
- `--openclaw PATH` — OpenClaw home directory (default: `~/.openclaw`)

### What gets created

| What | Where |
|------|-------|
| Skill | `~/.openclaw/skills/memory-boost/SKILL.md` |
| Template | `~/.openclaw/memory/TEMPLATE.md` |
| Task index | `~/.openclaw/memory/TASK-INDEX.md` |
| Loop state | `~/.openclaw/memory/LOOP-STATE.md` |
| Task folders | `~/.openclaw/memory/tasks/<task-name>/` |

| Job | Schedule | Purpose |
|-----|----------|---------|
| `boost-watchdog` | */15 * * * * | Detects stalls (only when loop armed) |
| `boost-replayer` | */30 * * * * | Takes one step on stalled task (only when loop armed) |
| `boost-escalator` | 0 * * * * | Forces restart on repeated stalls (only when loop armed) |
| `boost-validator` | 5 * * * * | Repairs missing notes, refreshes index (always runs) |
| `boost-smoke-test` | 0 */6 * * * | System health check (always runs) |

## Option 3: Manual install

1. Copy the `SKILL.md` file and `templates/`, `prompts/`, `examples/` directories into `~/.openclaw/skills/memory-boost/`.
2. Create `~/.openclaw/memory/tasks/`.
3. Copy `templates/TEMPLATE.md` and `templates/LOOP-STATE.md` into `~/.openclaw/memory/`.
4. Copy `examples/TASK-INDEX.md` into `~/.openclaw/memory/`.
5. Create the 5 cron jobs using `openclaw cron add` (see table above).

## How to use

**Task memory is automatic.** Once installed, your agent creates RESUME/CHECKLIST/DOCS notes for every task. The validator keeps them healthy. No action needed.

**The keep-alive loop is on-demand.** For long tasks:

1. `/loop-start` — arm the loop
2. Give your agent a task
3. Walk away — the loop keeps it alive
4. `/loop-stop` when done — stops burning tokens

## Verify

Ask your OpenClaw agent:

> Run the memory boost smoke test now.

It should return `smoke-test: pass` if everything is set up correctly.

## Uninstall

```bash
rm -rf ~/.openclaw/skills/memory-boost
openclaw cron remove --name "boost-watchdog"
openclaw cron remove --name "boost-replayer"
openclaw cron remove --name "boost-escalator"
openclaw cron remove --name "boost-validator"
openclaw cron remove --name "boost-smoke-test"
```

The memory notes in `~/.openclaw/memory/` are yours to keep or delete.
