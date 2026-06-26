# Scheduling Guide

## Recommended: Shell Script + System Cron

### Setup
1. Create run script:
   ~/.claude/skills/autoloop-controller/scripts/run-eval.sh

2. Add to crontab:
   17 */4 * * * ~/.claude/skills/autoloop-controller/scripts/run-eval.sh /path/to/skill /path/to/state

### Advantages
- No 7-day expiry
- Runs regardless of REPL state
- Production-grade reliability

## Alternative: CronCreate (session-based)
- 7-day auto-expiry (must re-register)
- Only fires when REPL is idle
- Good for ad-hoc experimentation

## Alternative: Continuous Mode
- Runs in current session with cooldown between iterations
- Best for supervised overnight runs
- Will stop on termination conditions
