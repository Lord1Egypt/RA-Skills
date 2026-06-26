# 🛡️ Aegis Protocol

**Self-Healing Stability Monitor for AI Agents**

[![Version](https://img.shields.io/badge/version-v0.7.0-blue)]()
[![Python](https://img.shields.io/badge/python-3.10+-blue)]()
[![Coverage](https://img.shields.io/badge/coverage-82%-green)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

---

## 🎯 What It Does

Prevents AI agents from silently dying. Aegis Protocol provides **20-dimension real-time monitoring** with **automatic fault recovery** and **quantifiable health scoring**.

Built for OpenClaw. Production ready.

---

## ✨ Features

### 5 Core Checks (Default)

### ⚠️ Limitations

- **Notifications**: Log output only (no push to Telegram/Slack/Feishu)
  - **You can configure**: Log collection (ELK, Loki) or custom notification script
- **Scheduling**: Manual cron setup required
  - **You can configure**: Add cron job for automatic periodic checks
- **Interface**: CLI only (no WebUI)
  - **You can use**: Log viewers like `lnav`, `multitail` for better CLI experience
  - **Planned**: WebUI in v1.1.0
- **External Calls**: Disabled (security)
  - **Advanced users**: Can enable by modifying code

| Check | Recovery |
|-------|----------|
| Sessions stuck | Kill session |
| LLM timeout | Alert user |
| Nginx down | Restart |
| Cron missing | Alert |
| PM2 alerts | Restart |

### 15 Extended Checks (--full)

| Category | Checks |
|----------|--------|
| System | Disk, Memory, CPU, Zombies, FD, Connections |
| Services | Docker |
| Security | SSL, Updates, Git |
| Maintenance | Backup, Cleanup, Network, Task Stalls, Loops |

| Category | Checks |
|----------|--------|
| **System** | CPU load, Memory, Disk, Zombie processes, Open files, Network connections |
| **Services** | PM2, Nginx, Docker containers, Cron tasks |
| **AI Agent** | Stuck sessions, Context usage, Task stalls, Infinite loops |
| **Security** | SSL certificates, Security updates, Git changes |
| **Maintenance** | Backup status, Cleanup suggestions, Network connectivity |

### Auto Recovery

- Terminate stuck sessions automatically
- Restart failed services
- Compact context before overflow
- Record recovery strategies in Healing Memory

### Health Scoring

- Quantified health score (0-100)
- Real-time status dashboard
- Historical trend tracking

---

## 🚀 Quick Start

### Install

```bash
# From ClawHub
clawhub install aegis-protocol

# Or manual
git clone https://github.com/mrring88/aegis-protocol.git
cp -r aegis-protocol ~/.openclaw/workspace/skills/
```

### Initialize

```bash
python3 aegis-protocol.py init
```

### Usage

```bash
# Check system health
python3 aegis-protocol.py check

# View status summary
python3 aegis-protocol.py status

# Auto recover issues
python3 aegis-protocol.py heal

# View configuration
python3 aegis-protocol.py config
```

---

## 📊 Example Output

```
============================================================
Aegis Protocol Status Check
============================================================
✅ sessions: {"status": "ok", "stuck_count": 0}
✅ pm2: {"status": "ok", "services": ["nevmatrix"]}
✅ nginx: {"status": "ok", "active": true}
✅ disk: {"status": "ok", "usage_percent": 45}
✅ memory: {"status": "ok", "usage_percent": 50}
✅ context: {"status": "ok", "usage_percent": 0}
✅ task_stall: {"status": "ok", "stalled_tasks": []}
✅ loop: {"status": "ok", "loop_detected": false}
------------------------------------------------------------
Summary: 8 ok / 0 warning / 0 error / 0 info
Health Score: 100/100
```

---

## 🧠 Healing Memory

Aegis learns from every recovery:

```json
{
  "strategyStats": {
    "session_kill": {"attempts": 10, "successes": 10},
    "service_restart": {"attempts": 5, "successes": 4},
    "context_compact": {"attempts": 3, "successes": 3}
  }
}
```

Success rates inform future recovery decisions.

---

## ⚙️ Configuration

Edit `~/.openclaw/workspace/.watchdog-config.json`:

```json
{
  "thresholds": {
    "sessionTimeoutMinutes": 60,
    "pm2RestartAlert": 50,
    "diskUsagePercent": 90,
    "memoryUsagePercent": 95,
    "contextUsagePercent": 80
  },
  "cooldowns": {
    "sessionKill": 300,
    "serviceRestart": 600,
    "contextCompact": 300
  }
}
```

---

## 🧪 Testing

```bash
# Run unit tests
python3 -m pytest tests/ -v

# Run integration tests
python3 -m pytest tests/test_integration.py -v
```

**Coverage**: 82%  
**Tests**: 20+ passing

---

## 📈 Performance

| Metric | Value |
|--------|-------|
| Check latency | <2s |
| Cache hit rate | ~80% |
| Cache TTL | 5 minutes |
| Memory footprint | <50MB |
| CPU usage | <1% idle |

---

## 🛠️ Development

```bash
# Clone repository
git clone https://github.com/mrring88/aegis-protocol.git
cd aegis-protocol

# Run tests
python3 -m pytest tests/ -v --cov=aegis_protocol

# Check code quality
python3 -m py_compile aegis-protocol.py
```

---

## 📝 Changelog

### v0.7.0 (2026-04-05)
- ✅ Result caching with TTL
- ✅ Type hints >90% coverage
- ✅ Exception classification (4 types)
- ✅ 20-dimension monitoring
- ✅ Health scoring system

### v0.6.6 (2026-04-05)
- ✅ Phase 2 code quality improvements
- ✅ Test coverage 82%
- ✅ API documentation complete

### v0.4.0 (2026-04-05)
- ✅ 20-dimension monitoring complete
- ✅ Health score 94-100/100

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## ❓ FAQ

### Q: Why no push notifications?

A: To avoid security false positives in ClawHub. 

**You can configure it yourself**:
- Option 1: Log collection (ELK, Loki, Graylog)
- Option 2: Cron + custom notification script
- Option 3: Logrotate + webhook

Ask your AI agent: "Help me set up notifications for Aegis Protocol"

### Q: How do I set up scheduled checks?

A: Use cron. See [Setup Scheduled Execution](#setup-scheduled-execution-recommended) above.

**Quick setup**:
```bash
crontab -e
# Add: */10 * * * * python3 /path/to/aegis-protocol.py heal >> /var/log/aegis-protocol.log 2>&1
```

Ask your AI agent: "Help me configure cron for Aegis Protocol"

### Q: Is there a WebUI?

A: Not yet. Planned for v1.1.0. 

**Alternatives**:
- `tail -f /var/log/aegis-protocol.log` - Real-time logs
- `lnav /var/log/aegis-protocol.log` - Log viewer with syntax highlighting
- `multitail /var/log/aegis-protocol.log` - Multi-file log viewer

Ask your AI agent: "What are the best tools for viewing Aegis logs?"

### Q: Can I monitor multiple servers?

A: Not yet. Planned for v1.3.0. For now, install on each server separately.

**Workaround**: Install Aegis on each server, aggregate logs centrally (rsync, ELK, etc.)

Ask your AI agent: "Help me set up multi-server monitoring with Aegis Protocol"

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- [OpenClaw](https://github.com/openclaw/openclaw) - Base framework
- [AURA](https://github.com/haribhaski/agentic-self-healing-ai-platform) - Self-healing architecture inspiration
- [amux](https://github.com/mixpeek/amux) - Watchdog design reference

---

*Aegis Protocol - The Never-Sleeping Guardian* 🌀  
**Version**: v0.7.0 · **Status**: Production Ready
