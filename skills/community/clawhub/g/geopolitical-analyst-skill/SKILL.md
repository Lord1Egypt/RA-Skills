---
name: geopolitical-analyst
description: Live geopolitical intelligence analysis with 39 analytical modules and real-time data integration. No API keys required.
version: 1.1.0
author: Nima Ansari
license: MIT
repository: https://github.com/nimaansari/geopolitical-analyst-skill
tags:
  - intelligence-analysis
  - geopolitical
  - scenario-planning
  - conflict-analysis
  - live-data
  - open-source
---

# Geopolitical Analyst Intelligence Framework

Analyzes any geopolitical situation using live data from 5 public APIs and 39 analytical modules. No API keys or credentials required.

## What This Skill Does

- **39 analytical modules** — game theory, escalation dynamics, historical patterns, sanctions analysis
- **9-step intelligence workflow** — data → bias → actors → economics → networks → patterns → info warfare → red team → scenarios
- **5 live data sources** — GDELT, ACLED, ReliefWeb, Frankfurter, UN Sanctions (all public, no keys)
- **Multi-perspective scenarios** — base case, upside, downside, catastrophic
- **Confidence scoring** — explicit uncertainty tracking

## Usage

### Setup (one time)

```bash
pip install -r requirements.txt
```

### Interactive Mode

```bash
python3 interactive_monitor.py
```
Then type any country or region: `Gaza`, `Ukraine`, `Taiwan`, `South China Sea`

### Command Line

```bash
python3 interactive_monitor.py "South China Sea" FULL
python3 interactive_monitor.py Ukraine BRIEF
```

### Python API

```python
from geopolitical_analyst_agent import run_analysis

result = run_analysis(
    country="Ukraine",
    keywords=["Ukraine", "Russia", "military"],
    depth="FULL"
)
```

## Files Included

| File | Purpose |
|------|---------|
| `geopolitical_analyst_agent.py` | Core analysis engine |
| `interactive_monitor.py` | Interactive CLI interface |
| `automated_monitor.py` | Scheduled monitoring |
| `data_fetchers.py` | Live API data fetching |
| `data_sources.py` | API source definitions |
| `modules_loader.py` | 39 analytical modules loader |
| `requirements.txt` | Python dependencies (requests, python-dateutil) |
| `references/` | 39 analytical module definitions |

## Dependencies

- `requests` >=2.28.0 — HTTP requests (standard library)
- `python-dateutil` >=2.8.2 — Date parsing (standard library)

Both are widely-used, well-maintained packages.

## Data Sources (All Public, No Keys)

| API | Rate Limit | Data |
|-----|-----------|------|
| GDELT | 250/day | News articles, sentiment |
| ACLED | 1,000/day | Conflict events, casualties |
| ReliefWeb | 100/day | Humanitarian data |
| Frankfurter | Unlimited | Currency rates |
| UN OFAC | Unlimited | Sanctions regimes |

## Security

- ✅ No API keys or credentials required
- ✅ All data sources are public APIs
- ✅ No data sent to external servers
- ✅ MIT licensed, fully open source
- ✅ Local processing only
- ✅ No system file modifications
