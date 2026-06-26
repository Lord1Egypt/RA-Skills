---
name: cwd-guardian
description: Monitors and restores the evolver process working directory. Use when evolver crashes with uv_cwd ENOENT errors or when the evolver process loses its cwd.
---

# cwd-guardian

Protects the evolver daemon from `uv_cwd ENOENT` crashes by:
1. Stamping the current valid cwd to a pidfile
2. On restart, verifying the cwd exists before launching evolver
3. Rebuilding the cwd from the stamped path if it was deleted

## Usage

```bash
node skills/cwd-guardian/scripts/guardian.js start
node skills/cwd-guardian/scripts/guardian.js check
```

## Logic

- `start`: Records current working directory to `~/.openclaw/workspace/memory/evolution/cwd_guardian.pid`, then starts the evolver daemon
- `check`: Reads the pidfile, verifies the cwd exists, recreates it if missing, then starts the evolver daemon if not running
- `verify`: Returns exit code 0 if cwd is valid, 1 if recreated
