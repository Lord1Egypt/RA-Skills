---
slug: "drift-guard-sr"
name: "Drift Guard: Agent Behavior Monitor"
description: "Detect personality drift, sycophancy creep, and capability degradation in AI agents before they become problems. Tracks behavior metrics over time against healthy baselines."
author: "@TheShadowRose"
version: "1.0.3"
tags: ["drift-detection", "personality", "sycophancy", "monitoring", "behavior", "quality-control"]
license: "MIT"
---

# Drift Guard Agent Behavior Monitor

Detect personality drift, sycophancy creep, and capability degradation in AI agents before they become problems. Tracks behavior metrics over time against healthy baselines.

---

**Detect personality drift, sycophancy creep, and capability degradation in AI agents before they become problems.**

Drift Guard tracks agent behavior metrics over time, compares them against healthy baselines, and alerts you when your agent starts drifting from its intended personality or capability level.

---

## The Problem

AI agents evolve during use. Sometimes that evolution is productive learning. Sometimes it's drift into undesirable behaviors:

- **Personality drift:** Agent becomes more verbose, changes tone, loses its edge
- **Sycophancy creep:** Excessive agreement, validation-seeking, compliment inflation
- **Capability degradation:** Hedging language increases, technical depth decreases, confidence drops
- **Memory pollution:** Corrupted context files influence all future responses

You don't notice it happening until your sharp, capable agent has turned into a people-pleasing chatbot.

## What Drift Guard Does

### 1. **Baseline Capture** (`drift_baseline.py`)
- Record "healthy" agent behavior from known-good responses
- Analyze multiple samples to create robust baseline metrics
- Store baseline for ongoing comparison
- Compare baselines over time to track evolution

### 2. **Continuous Monitoring** (`drift_guard.py`)
- Analyze each agent response for behavior metrics
- Calculate drift score against baseline (0.0 = perfect, 1.0 = complete drift)
- Track metrics: response length, vocabulary diversity, sycophancy markers, hedging language, technical depth
- Record all measurements with timestamps
- Trigger alerts when drift exceeds configured thresholds

### 3. **Trend Analysis** (`drift_report.py`)
- Generate drift trend reports over time
- Detect anomalies (outlier measurements)
- Identify which specific metrics are changing
- Track whether drift is worsening or improving
- Time-range filtering (last 24h, last week, all time)

---

## Quick Start

### 1. Configure

```bash
cp config_example.py config.py
# Edit config.py with your thresholds, patterns, and alert settings
```

### 2. Capture Baseline

Collect 10-20 agent responses that represent your agent's "healthy" behavior. Save each to a text file.

```bash
python drift_baseline.py capture --files response1.txt response2.txt response3.txt \
  --output baseline.json
```

### 3. Monitor

Each time your agent responds, analyze it:

```bash
python drift_guard.py agent_response.txt
```

Or pipe from stdin:

```bash
echo "Agent response here..." | python drift_guard.py --stdin
```

### 4. Review Trends

```bash
# Last 24 hours
python drift_report.py --hours 24

# All time
python drift_report.py

# JSON output for scripting
python drift_report.py --format json
```

---

## Integration Examples

### Integration with Agent Workflow

```python
from drift_guard import DriftGuard

# Load config
from config import CONFIG
dg = DriftGuard(CONFIG)

# After agent responds
agent_response = "..."
result = dg.monitor(agent_response)

if result['alert_level'] == 'critical':
    print(f"ALERT: Agent drift detected ({result['drift_score']:.3f})")
    # Trigger recovery: load checkpoint, reset memory, etc.
```

### Automatic Drift Checks via Cron

```bash
# Check drift every hour
0 * * * * cd /path/to/agent && python drift_guard.py latest_response.txt

# Weekly drift report
0 9 * * 1 cd /path/to/agent && python drift_report.py --hours 168 > weekly_drift.txt
```

### Pairing with CPR (Context Preservation & Restore)

Drift Guard detects the problem. CPR fixes it.

```bash
# Monitor drift
python drift_guard.py agent_response.txt
# Drift score: 0.72 (CRITICAL)

# Restore from checkpoint
python cpr.py restore --checkpoint 2024-01-15-healthy

# Verify recovery
python drift_guard.py agent_response.txt
# Drift score: 0.12 (normal)
```

---

## How It Works

### Metrics Tracked

| Metric | What It Measures | Why It Matters |
|--------|------------------|----------------|
| `char_count` | Response length in characters | Verbosity drift |
| `word_count` | Response length in words | Verbosity drift |
| `sentence_count` | Number of sentences | Structure changes |
| `avg_sentence_length` | Words per sentence | Complexity drift |
| `vocabulary_diversity` | Unique words / total words | Language degradation |
| `sycophancy_score` | Frequency of agreement/validation language | People-pleasing behavior |
| `hedging_score` | Frequency of uncertainty language | Confidence degradation |
| `validation_score` | Frequency of compliments/encouragement | Sycophancy creep |
| `exclamation_count` | Number of exclamation marks | Enthusiasm drift |
| `technical_score` | Frequency of technical terminology | Capability tracking |

### Drift Score Calculation

For each metric:
1. Calculate percentage difference from baseline
2. Apply configured weight (important metrics count more)
3. Average weighted differences across all metrics
4. Result: drift score from 0.0 (perfect baseline match) to 1.0 (completely different)

### Alert Levels

- **Warning (0.3):** Minor drift detected. Monitor closely.
- **Critical (0.6):** Significant drift. Intervention recommended.
- **Emergency (0.9):** Severe drift. Immediate action required.

---

## Use Cases

- **Personality preservation:** Ensure your agent maintains its configured tone and style
- **Quality monitoring:** Detect when response quality degrades over time
- **Context corruption detection:** Identify when bad memory files are influencing behavior
- **Fine-tuning validation:** Verify fine-tuned models maintain desired characteristics
- **Multi-agent consistency:** Monitor multiple agents to ensure behavioral consistency
- **Recovery triggers:** Automatically restore from checkpoint when drift exceeds threshold

---

## What's Included

| File | Purpose |
|------|---------|
| `drift_guard.py` | Main monitoring engine |
| `drift_baseline.py` | Baseline capture and comparison |
| `drift_report.py` | Trend analysis and reporting |
| `config_example.py` | Configuration template |
| `LIMITATIONS.md` | What Drift Guard doesn't do |
| `LICENSE` | MIT License |

---

## Requirements

- Python 3.8+
- No external dependencies (stdlib only)
- Works with any AI agent that generates text responses

---

## quality-verified


---

## License

MIT — See `LICENSE` file.

**Author:** Shadow Rose


---

## ⚠️ Disclaimer

This software is provided "AS IS", without warranty of any kind, express or implied.

**USE AT YOUR OWN RISK.**

- The author(s) are NOT liable for any damages, losses, or consequences arising from 
  the use or misuse of this software — including but not limited to financial loss, 
  data loss, security breaches, business interruption, or any indirect/consequential damages.
- This software does NOT constitute financial, legal, trading, or professional advice.
- Users are solely responsible for evaluating whether this software is suitable for 
  their use case, environment, and risk tolerance.
- No guarantee is made regarding accuracy, reliability, completeness, or fitness 
  for any particular purpose.
- The author(s) are not responsible for how third parties use, modify, or distribute 
  this software after purchase.

By downloading, installing, or using this software, you acknowledge that you have read 
this disclaimer and agree to use the software entirely at your own risk.


**DATA DISCLAIMER:** This software processes and stores data locally on your system. 
The author(s) are not responsible for data loss, corruption, or unauthorized access 
resulting from software bugs, system failures, or user error. Always maintain 
independent backups of important data. This software does not transmit data externally 
unless explicitly configured by the user.

---

## Support & Links

| | |
|---|---|
| 🐛 **Bug Reports** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*Built with [OpenClaw](https://github.com/openclaw/openclaw) — thank you for making this possible.*

---

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at $500. If you can describe it, I can build it. → [Hire me on Fiverr](https://www.fiverr.com/s/jjmlZ0v)