# Context Guardian 🛡️

**Your context guardian. Alerts before errors happen.**

Proactive context monitoring with smart 3-level alerts (60%, 70%, 85%). Know when to restart before quality degrades.

## Features

- 🛡️ **Proactive protection** against context pollution
- 📊 **Real-time monitoring** with zero overhead
- 🚨 **Smart 3-level alerts** (60%, 70%, 85%)
- 🔧 **Highly configurable** thresholds and alert styles
- 🤝 **Integrates** with context-optimizer and context-recovery

## Quick Start

1. Install:
   ```bash
   clawhub install context-guardian
   ```

2. Add to `HEARTBEAT.md`:
   ```markdown
   ## Context Monitoring
   - Check context usage via context-guardian
   ```

3. Done! You'll get alerts when context usage reaches thresholds.

## Why You Need This

Long conversations lead to context pollution. Quality degrades silently as context fills up. You don't know when to restart until it's too late.

Context Guardian monitors your context usage and alerts you **before** errors happen:

- ⚠️ **60%** - Warning: Consider wrapping up
- 🟠 **70%** - Danger: Finish current task, start fresh
- 🔴 **85%** - Critical: High error risk, restart NOW

## Documentation

See [SKILL.md](SKILL.md) for full documentation.

## License

MIT
