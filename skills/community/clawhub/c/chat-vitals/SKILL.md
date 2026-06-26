---
name: chat-vitals
version: "1.1.0"
description: |
  Chat Vitals - Monitor chat conversation health with real-time insights.
  
  Tracks conversation quality metrics: first-try success rate, promise 
  fulfillment, token efficiency, and detects inefficiencies like rework 
  and plan inflation.
  
  Features:
  - Auto-collect: Zero-friction conversation tracking
  - Real-time dashboard: Live health monitoring with visual indicators
  - Health scoring: 4-tier system (🟢🟡🟠🔴)
  - Actionable reports: Optimization suggestions based on data
  
  Keywords: chat monitoring, LLM health, conversation quality, token 
  efficiency, AI performance, real-time dashboard, vitals
metadata:
  author: "OpenClaw Community"
  license: "MIT"
  openclaw:
    emoji: "📊"
    category: "utility"
    tags: ["chat", "monitoring", "vitals", "analytics", "performance", "dashboard"]
    requires:
      bins: ["python3"]
      python: ">=3.8"
    compatibility:
      openclaw: ">=0.9.0"
---

# 📊 Chat Vitals v1.1.0

> Monitor your AI conversation health like a doctor checks vital signs. 
> **Auto-collection + Real-time dashboard + Actionable insights.**

## ✨ What's New in v1.1.0

### 🚀 Auto-Collection (Zero Friction)
**Before**: Manual tracking for every turn  
**Now**: One command, automatic tracking

```bash
vitals start claude-sonnet-4.6
# All conversations tracked automatically!
```

### 🖥️ Real-Time Dashboard
Live terminal UI with health monitoring:

```bash
vitals dashboard
```

Shows:
- ⚡ Live health score (0-100) with color coding
- 📊 Real-time metrics refresh
- 🚨 Instant alerts for problems
- 📈 Token usage tracking

## 🚀 Quick Start

```bash
# 1. Start monitoring (one command!)
vitals start claude-sonnet-4.6

# 2. View real-time dashboard (in another terminal)
vitals dashboard

# 3. Check status anytime
vitals status

# 4. Generate report when done
vitals report
```

## 📋 All Commands

| Command | Description |
|---------|-------------|
| `vitals start [model]` | Start auto-monitoring session |
| `vitals dashboard` | Launch real-time dashboard |
| `vitals status` | Show current session status |
| `vitals summary` | Quick session summary |
| `vitals complete` | Mark session as complete |
| `vitals report` | Generate detailed report |

## 🎯 Core Metrics

| Metric | Description | Healthy | Warning | Danger |
|--------|-------------|---------|---------|--------|
| **First-Try Success** | % tasks without rework | ≥70% | 50-70% | <50% |
| **Rework Count** | Corrections per task | 0 | 1-2 | >2 |
| **Promise Fulfillment** | % promises delivered | ≥80% | 60-80% | <60% |
| **Plan Inflation** | Actual / Promised turns | ≤1.3x | 1.3-2.0x | >2.0x |
| **Token Efficiency** | Value per token | ≥0.15 | 0.08-0.15 | <0.08 |

## 🏥 Health Status

| Score | Status | Emoji | Color |
|-------|--------|-------|-------|
| 85-100 | Excellent | 🟢 | Green |
| 70-84 | Good | 🟡 | Yellow |
| 50-69 | Warning | 🟠 | Orange |
| <50 | Critical | 🔴 | Red |

## 📊 Sample Output

```
📊 Chat Vitals Dashboard
──────────────────────────────────────────────────

Session: a1b2c3d4
Model:   claude-sonnet-4.6
Started: 2026-04-08T11:34:27

Health Score:
🟢 85/100 - Excellent
[██████████████████████████████] 85%

Key Metrics:
──────────────────────────────────────────────────
  ✅ First-Try Success: 85%
  ✅ Rework Count: 0
  ⚠️  Promise Fulfillment: 75%
  ✅ Plan Inflation: 1.1x
  ✅ Token Efficiency: 0.22

Session Stats:
  💬 Total Turns: 3
  🔢 Total Tokens: 1,030
  📊 Avg Tokens/Turn: 343
```

## ⚙️ Configuration

Edit `~/.openclaw/skills/chat-vitals/config.json`:

```json
{
  "monitor": {
    "token_thresholds": {
      "report_daily": 50000
    },
    "health_thresholds": {
      "first_try_success_rate": {
        "excellent": 85,
        "good": 70,
        "warning": 50
      }
    }
  },
  "patterns": {
    "correction_keywords": ["不对", "错了", "重新"],
    "promise_patterns": ["接下来我会", "首先让我"]
  }
}
```

## 📁 Project Structure

```
chat-vitals/
├── vitals                  # ⭐ Simple CLI entry point
├── SKILL.md
├── README.md
├── config.json
├── scripts/
│   ├── collector.py        # Core data collection
│   ├── analyzer.py         # Metric analysis
│   ├── reporter.py         # Report generation
│   ├── auto_collector.py   # ⭐ Auto-collection
│   └── dashboard.py        # ⭐ Real-time dashboard
└── tests/
    └── test_vitals.py      # Test suite
```

## 🧪 Testing

```bash
cd ~/.openclaw/skills/chat-vitals
./tests/run_tests.sh

# Test new features
vitals start test-model
vitals status
vitals dashboard  # In a real terminal
```

## 🔌 Advanced Usage

### Legacy Manual Mode

```bash
python3 scripts/collector.py create ...
python3 scripts/collector.py record ...
python3 scripts/collector.py complete ...
```

### Programmatic Access

```python
from llmchat_vitals.scripts import auto_collector

# Start monitoring
auto_collector.auto_start_session("gpt-4")

# Record turn
auto_collector.auto_record_turn(user_input, model_output)

# Get live summary
summary = auto_collector.get_session_summary()
print(f"Health: {summary['health_score']}/100")
```

## 🛣️ Roadmap

- [x] Auto-collection (v1.1.0)
- [x] Real-time dashboard (v1.1.0)
- [x] Simplified CLI (v1.1.0)
- [ ] Webhook integrations (Feishu/Slack)
- [ ] Intent drift detection
- [ ] Web dashboard
- [ ] Multi-model comparison
- [ ] Prompt optimization suggestions

## 🤝 Contributing

Issues and PRs welcome!

## 📄 License

MIT License
