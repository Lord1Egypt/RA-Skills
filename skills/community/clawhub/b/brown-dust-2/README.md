# 🎮 Brown Dust 2 Automation

[![ClawHub](https://img.shields.io/badge/ClawHub-brown--dust--2-blue)](https://clawhub.ai)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-brightgreen)](https://python.org)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-orange)]()
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Brown Dust 2 全自动签到 + 兑换码一键兑换 for [OpenClaw](https://openclaw.ai).

## Features

### Web Shop Sign-in (API-based)

- Daily attendance reward (free item every day)
- Weekly attendance reward
- Event attendance (7-day login event)
- All via direct API calls — no browser automation needed

### Gift Code Redemption (API-based)

- Auto-scrape latest codes from [BD2Pulse](https://thebd2pulse.com)
- One-click redeem all codes via official API
- Reports: new success / already redeemed / expired

## Install

```bash
clawhub install brown-dust-2
```

Or clone:

```bash
git clone https://github.com/XiaoYiWeio/brown-dust-2.git ~/.openclaw/workspace/skills/brown-dust-2
```

## Setup

### Sign-in (one-time token setup)

1. Log in to [BD2 Web Shop](https://webshop.browndust2.global/CT/) with Google
2. Press F12 → Console → paste:
   ```js
   JSON.parse(localStorage.getItem("session-storage")).state.session.accessToken
   ```
3. Save the token:
   ```bash
   python3 scripts/signin.py --save-token "YOUR_TOKEN"
   ```

### Gift Code (one-time nickname setup)

```bash
python3 scripts/redeem.py --save-nickname "YourNickname"
```

## Usage

### In OpenClaw

- "BD2签到" — daily/weekly/event sign-in
- "BD2兑换码" — auto-redeem all latest codes
- "BD2全签" — sign-in + redeem codes

### CLI

```bash
# Sign-in (daily + weekly + event)
python3 scripts/signin.py

# Check event info
python3 scripts/signin.py --event-info

# Daily only
python3 scripts/signin.py --daily-only

# Redeem all codes
python3 scripts/redeem.py

# List codes without redeeming
python3 scripts/redeem.py --list

# JSON output (both scripts support --json)
python3 scripts/signin.py --json
```

## Architecture

```
brown-dust-2/
├── SKILL.md          # OpenClaw skill definition
├── persona.md        # Agent interaction guide
├── README.md
└── scripts/
    ├── signin.py     # Web shop sign-in (daily/weekly/event)
    └── redeem.py     # Gift code scraper + redeemer
```

## How It Works

This skill reverse-engineered the official BD2 Web Shop API:

| Function | API | Auth |
|----------|-----|------|
| Daily attend | `POST /api/user/attend {type:0}` | Bearer token |
| Weekly attend | `POST /api/user/attend {type:1}` | Bearer token |
| Event attend | `POST /api/event/attend-reward` | Bearer token |
| Event info | `GET /api/event/event-info` | None |
| Gift code redeem | `POST coupon API` | None (nickname only) |

## License

MIT
