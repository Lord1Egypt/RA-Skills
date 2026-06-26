# 🛡️ Dreaming Guard Pro

> Smart prevention and auto-recovery for OpenClaw dreaming context overflow

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-green.svg)](https://clawhub.ai)

## 🎯 Problem

OpenClaw's dreaming mechanism can accumulate context files indefinitely, leading to:
- 💥 OOM crashes (gateway process consuming all memory)
- 🐌 Performance degradation
- 🔄 Unrecoverable sessions
- 😡 Frustrated users losing work

Official fix (PR#67697) is still pending. This project provides a **complete prevention and recovery solution** today.

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📊 **Real-time Monitoring** | Track file count, size, growth rate, process memory |
| 🔮 **Trend Prediction** | Forecast when dreaming will overflow based on growth patterns |
| 🗄️ **Smart Archiving** | 3-tier archival: hot (7d) → warm (30d) → cold (30d+) with gzip compression |
| 🗜️ **Semantic Compression** | 3-level: lossless (dedup) → lossy (summarize) → aggressive (key info only) |
| 🛡️ **Process Protection** | Monitor gateway RSS memory, intervene before OOM |
| 💊 **Crash Self-healing** | Auto-detect crashes, restore from health checkpoints |
| 📋 **Health Reports** | Regular status reports in text/JSON/markdown |
| ⚙️ **Configurable** | Custom thresholds, strategies, and notification channels |

## 🚀 Quick Start

### As OpenClaw Skill

```bash
clawhub install dreaming-guard-pro
```

### Standalone

```bash
git clone https://github.com/kuangzhanzhiwang/dreaming-guard-pro.git
cd dreaming-guard-pro
npm install  # No external dependencies needed!

# Run once
node src/guard.js --once

# Run as daemon
node src/guard.js --daemon

# Generate health report
node src/guard.js --report markdown
```

### Cron Setup

```bash
# Add to crontab (run every minute)
* * * * * /path/to/dreaming-guard-pro/scripts/dreaming-guard-pro.sh >> /tmp/dreaming-guard.log 2>&1
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│              Guard (Main Loop)           │
│  monitor → analyzer → decision → execute │
├─────────────────────────────────────────┤
│  Logger  │  Config  │  StateManager     │  Phase 1
├─────────────────────────────────────────┤
│  Monitor │ Archiver │  Compressor       │  Phase 2
├─────────────────────────────────────────┤
│  Analyzer │  Decision                   │  Phase 3
├─────────────────────────────────────────┤
│  Protector │  Healer                    │  Phase 4
├─────────────────────────────────────────┤
│  Reporter │  Guard                      │  Phase 5
└─────────────────────────────────────────┘
```

**12 modules, ~3000 lines, zero external dependencies.**

## 📊 Risk Levels & Actions

| Risk Level | Size Threshold | Memory | Action |
|-----------|---------------|--------|--------|
| 🟢 Green | < 50% | < 70% | Monitor only |
| 🟡 Yellow | 50-75% | 70-85% | Notify + Archive old files |
| 🔴 Red | 75-90% | 85-95% | Compress + Aggressive archive |
| ⚫ Emergency | > 90% | > 95% | Emergency cleanup + Gateway restart |

## ⚙️ Configuration

Create `~/.openclaw/dreaming-guard.json`:

```json
{
  "monitor": {
    "intervalMs": 60000,
    "dreamsDir": "~/.openclaw/dreams"
  },
  "thresholds": {
    "warningPercent": 50,
    "criticalPercent": 75,
    "emergencyPercent": 90,
    "memoryWarningPercent": 70,
    "memoryCriticalPercent": 85
  },
  "archiver": {
    "hotDays": 7,
    "warmDays": 30,
    "archiveDir": "~/.openclaw/dreaming-archive"
  },
  "compressor": {
    "defaultStrategy": "lossless"
  }
}
```

Environment variables (prefixed with `DREAMING_GUARD_`):

```bash
DREAMING_GUARD_MONITOR_INTERVALMS=30000
DREAMING_GUARD_THRESHOLDS_WARNINGPERCENT=40
```

## 🧪 Testing

```bash
# Run all tests
node test/run-tests.js        # Phase 1
node test/test-phase2.js      # Phase 2
node test/test-phase3.js      # Phase 3
node test/test-phase4.js      # Phase 4
node test/test-phase5.js      # Phase 5
```

## 🔄 Migration from dreaming-guard.sh

Dreaming Guard Pro is **backward compatible** with the original shell script:
- Reads the same dreams directory
- Archives to the same location
- Can coexist with the old cron job during migration

```bash
# Disable old script
crontab -l | grep -v dreaming-guard.sh | crontab -

# Enable new guard
* * * * * /path/to/dreaming-guard-pro/scripts/dreaming-guard-pro.sh
```

## 📄 License

Apache License 2.0 - see [LICENSE](LICENSE)

## 🤝 Contributing

Contributions welcome! This project helps the entire OpenClaw community deal with dreaming overflow.

## 🙏 Acknowledgments

- OpenClaw community for the dreaming mechanism
- All agents who suffered from OOM crashes 😢
