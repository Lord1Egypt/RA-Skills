# Fleece — Credit Card Research & Redemption

[![PyPI version](https://img.shields.io/pypi/v/fleece-cli?color=FFD100&label=fleece-cli)](https://pypi.org/project/fleece-cli/)
[![PyPI downloads](https://img.shields.io/pypi/dm/fleece-cli?color=FFD100)](https://pypi.org/project/fleece-cli/)
[![Python](https://img.shields.io/pypi/pyversions/fleece-cli?color=FFD100)](https://pypi.org/project/fleece-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-FFD100.svg)](https://github.com/chenyuan99/fleece/blob/main/LICENSE)
[![Publish to PyPI](https://github.com/chenyuan99/fleece/actions/workflows/publish.yml/badge.svg)](https://github.com/chenyuan99/fleece/actions/workflows/publish.yml)
[![ClawHub](https://img.shields.io/badge/ClawHub-fleece%401.5.0-FFD100)](https://clawhub.ai)
[![Website](https://img.shields.io/website?url=https%3A%2F%2Fgetfleece.io&color=FFD100&label=getfleece.io)](https://getfleece.io/)

> Find the best card for deal saviors.

Fleece is a free, open-source credit card research and award redemption toolkit. It provides live data via Brave Search — no stale training data. Every command outputs clean JSON, making it easy to plug into AI agent workflows.

---

## Quick Start

```bash
pip install fleece-cli
export BRAVE_API_KEY=<your_key>   # optional — offline commands work without it

fleece card "Amex Gold"           # full card report
fleece wallet                     # portfolio analysis
fleece mcc 5812                   # MCC lookup (no API key needed)
fleece flights JFK NRT --date 2026-06-01 --cabin business --open
```

## CLI Commands

### Research (requires `BRAVE_API_KEY`)

| Command | Description |
|---|---|
| `fleece card "<name>"` | Fees, welcome offer, earning rates, credits, benefits |
| `fleece rates "<name>"` | Earning rates by spend category |
| `fleece partners "<name>"` | Transfer partners, ratios, and timing |
| `fleece credits "<name>"` | Statement credits and perks |
| `fleece news "<name>"` | Recent changes (past month) |
| `fleece compare "<A>" "<B>"` | Side-by-side card comparison |
| `fleece wallet` | Portfolio analysis — coverage, overlaps, gaps |
| `fleece roi "<name>"` | First-year ROI estimate |
| `fleece recommend "<profile>"` | Personalized card recommendations |

### Offline (no API key needed)

| Command | Description |
|---|---|
| `fleece mcc <code>` | Look up a Merchant Category Code (981 codes bundled) |
| `fleece mcc <code> --wallet` | Cross-reference MCC with your saved cards |
| `fleece flights <ORIGIN> <DEST> --date <YYYY-MM-DD>` | PointsYeah award flight search URL |
| `fleece hotels "<location>" --checkin <date> --checkout <date>` | PointsYeah award hotel search URL |
| `fleece profile set <field> <value>` | Save your spending profile |
| `fleece profile show` | View your profile |

All commands support `--json` for agent-friendly output and `-` to read from stdin.

## Spending Profile

Set your profile once — `fleece wallet`, `fleece roi`, and `fleece recommend` use it automatically:

```bash
fleece profile set dining_monthly 600
fleece profile set travel_monthly 300
fleece profile set home_airport JFK
fleece profile set goal "business class to Tokyo 2027"
fleece profile set annual_fee_tolerance 550

fleece roi "Amex Gold"      # spend values pulled from profile
fleece wallet               # gap analysis tailored to your spend
```

## AI Agent Integration

### Claude Code
```bash
bash install.sh --claude
# Installs 13 slash commands: /fleece-card /fleece-wallet /fleece-mcc ...
```

### OpenClaw / Codex
```bash
bash install.sh --agents
# Installs .agents/skills/fleece/SKILL.md
```

### ClawHub Registry
```bash
clawhub install fleece   # fleece@1.5.0
```

## Chatbot

A Streamlit conversational interface is also included:

```bash
pip install -r requirements.txt
OPENAI_API_KEY=<key> streamlit run fleece.py
```

## Development

```bash
git clone https://github.com/chenyuan99/fleece.git
cd fleece
pip install -e .
export BRAVE_API_KEY=<your_key>
fleece --help
```

### Running tests
```bash
pip install pytest
pytest -q
```

## License

MIT — see [LICENSE](LICENSE)

## Author

[@chenyuan99](https://github.com/chenyuan99) · [getfleece.io](https://getfleece.io/)
