# Dial-a-Cron

**Stateful, intelligent cron orchestration for OpenClaw.**

## What is it?

Dial-a-Cron wraps regular cron jobs with enterprise features:
- Persistent memory between runs
- Automatic change detection (skip if output is identical)
- Smart delivery routing based on severity
- Token budget tracking and enforcement
- Self-healing with automatic retries and pause-on-failure

It turns basic scheduled tasks into reliable, self-aware agents.

## Features

- **Persistent State**: Remembers previous results and statistics
- **Change Detection**: Skips execution when nothing has changed
- **Smart Routing**: Routes output to different channels (success/warning/error)
- **Budget Control**: Tracks and respects token usage limits
- **Self-Healing**: Automatic retries, backoff, and auto-pause after failures

## Quick Start

### Basic Usage
```bash
# Create a stateful cron with change detection
openclaw cron create --name daily-summary \
  --command "python generate_report.py" \
  --dial "state:yes,change-detection:yes"
```

### Advanced Usage
```bash
# Full featured cron with routing and budget control
openclaw cron create --name system-monitor \
  --command "openclaw healthcheck" \
  --dial "state:yes,routing:telegram:error,slack:warning,budget:50000,self-heal:yes"
```

## Configuration Options

- `state:yes` — Enable persistent memory between runs
- `change-detection:yes` — Skip if output hasn't changed
- `routing:<channel>:<level>` — Route output by severity
- `budget:<number>` — Set token budget limit
- `self-heal:yes` — Enable automatic retry and recovery

## Core Engine

The main logic is in `scripts/dial-a-cron.py`. The skill automatically registers itself with OpenClaw's cron system.

## Use Cases

- Monitoring and alerting systems
- Data pipeline orchestration
- Report generation
- System maintenance tasks
- Any scheduled job that benefits from memory and intelligence

---

**Part of the OpenClaw ecosystem.**  
Clean, production-ready cron intelligence.
