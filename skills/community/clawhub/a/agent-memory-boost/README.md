# Memory Boost for OpenClaw

Give your OpenClaw agent a memory that never dies and a heartbeat monitor that never sleeps.

**Task memory** — every task your agent works on automatically gets persistent RESUME, CHECKLIST, and DOCS notes. Work survives restarts, context loss, and session changes.

**Keep-alive loop** — for long tasks, arm the loop and walk away. If your agent stalls, the loop detects it and keeps work moving. Disarm when done so you're not burning tokens.

```
/loop-start   <- arm before a long task
/loop-stop    <- disarm when done
```

No external dependencies. No Obsidian. Everything lives inside `~/.openclaw/memory/`.

## The problem

1. Agent tasks lose state when sessions end or context compacts. You restart and everything is gone.
2. Long tasks fail silently. The agent stalls and nobody notices.

## How it works

### Task memory (always on)

Every time your agent gets a task, it creates a folder with three notes:
- **RESUME.md** — what the task is, current status, next action, how to restart
- **CHECKLIST.md** — step-by-step progress
- **DOCS.md** — decisions, gotchas, notes for the next session

A **validator** runs every hour to repair missing notes and keep a task index current. A **smoke test** runs every 6 hours to make sure the system itself is healthy.

### Keep-alive loop (arm when needed)

When you `/loop-start`, three monitoring layers activate:

| Layer | Schedule | What it does |
|-------|----------|--------------|
| **Watchdog** | Every 15m | Detects when your agent has stalled and writes a recovery note |
| **Replayer** | Every 30m | Picks up a stalled task and takes one concrete step forward |
| **Escalator** | Every 60m | Forces a fresh-session restart if the same stall keeps repeating |

When you `/loop-stop`, the monitoring jobs immediately stop. The task memory keeps running either way.

## Install

### From ClawHub

```bash
npx clawhub@latest install memory-boost
```

Then run the setup:
```bash
cd ~/.openclaw/skills/memory-boost
./install.sh
```

### From GitHub

```bash
git clone https://github.com/TechieTer/openclaw-memory-boost.git
cd openclaw-memory-boost
./install.sh
```

No arguments needed — everything installs to `~/.openclaw/` automatically.

See [INSTALL.md](INSTALL.md) for manual install, options, and uninstall.

## Usage

**Every task** (automatic — no action needed):
- Give your agent a task -> it creates RESUME/CHECKLIST/DOCS automatically
- The validator keeps notes healthy in the background

**Long tasks** (arm the loop):
1. `/loop-start`
2. Give your agent the task
3. Walk away — the loop keeps it alive
4. `/loop-stop` when done

## What gets created

```
~/.openclaw/memory/
  TEMPLATE.md          # canonical template for new task folders
  TASK-INDEX.md        # quick-scan index of all tasks
  LOOP-STATE.md        # armed/disarmed state marker
  tasks/
    <task-name>/
      RESUME.md
      CHECKLIST.md
      DOCS.md
```

## Also available for

- **Obsidian users**: [memory-keep-alive-for-obsidian](https://clawhub.ai/techieter/memory-keep-alive-for-obsidian) (OpenClaw + Obsidian)
- **Hermes users**: [hermes-memory-keep-alive-for-obsidian](https://github.com/TechieTer/hermes-memory-keep-alive-for-obsidian)

## License

MIT
