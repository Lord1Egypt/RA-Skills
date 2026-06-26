# 📺 Bili Checkin

[![ClawHub](https://img.shields.io/badge/ClawHub-bili--checkin-blue)](https://clawhub.ai)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-brightgreen)](https://python.org)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-orange)]()
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

B站全自动签到工具 for [OpenClaw](https://openclaw.ai)。每日经验任务 + 直播间弹幕签到，一句话搞定。

## Features

### Daily EXP Tasks (每日经验 +65)

| Task | EXP | Auto |
|------|-----|:----:|
| Login | +5 | ✅ |
| Watch video | +5 | ✅ |
| Share video | +5 | ✅ |
| Coin ×5 | +50 | ✅ (costs coins) |
| **Total** | **65** | |

### Live Room Danmaku (直播弹幕签到)

| Action | Intimacy | EXP |
|--------|----------|-----|
| Send danmaku | +2 | +5 |

### UP主 Lookup (主播查找)

Search by name, UID, space URL, or live URL — auto-resolve to room ID.

## Install

```bash
clawhub install bili-checkin
```

Or clone:

```bash
git clone https://github.com/XiaoYiWeio/bili-checkin.git ~/.openclaw/workspace/skills/bili-checkin
```

## Setup (One-time)

1. Log in to [bilibili.com](https://www.bilibili.com) in Chrome
2. Press F12 → Application → Cookies → bilibili.com
3. Copy **SESSDATA** and **bili_jct**
4. Save:

```bash
python3 scripts/checkin.py --save-cookie --sessdata "YOUR_SESSDATA" --bili-jct "YOUR_BILI_JCT"
```

## Usage

### In OpenClaw (Recommended)

Just say:
- "B站签到" / "每日任务"
- "帮我直播间签到 思诺snow"
- "B站全签"

### CLI

```bash
# Daily EXP tasks (all)
python3 scripts/daily.py

# Skip coin (save coins)
python3 scripts/daily.py --skip-coin

# Check status
python3 scripts/daily.py --status

# Live room danmaku
python3 scripts/checkin.py --room 30858592
python3 scripts/checkin.py --room 30858592 --msg "打卡"

# Multiple rooms
python3 scripts/checkin.py --room 30858592,22637261

# Lookup UP主
python3 scripts/lookup.py "思诺snow"
python3 scripts/lookup.py "3537115310721781"
```

## Architecture

```
bili-checkin/
├── SKILL.md          # OpenClaw skill definition
├── persona.md        # Agent interaction guide
├── README.md
└── scripts/
    ├── daily.py      # Daily EXP tasks (login+watch+share+coin+live sign)
    ├── checkin.py    # Live room danmaku check-in via API
    └── lookup.py     # UP主 → room_id resolver
```

## Design

- **Zero dependencies** — pure Python 3 standard library
- **Cookie-based API** — no browser automation needed, fast and reliable
- **One-time setup** — save cookie once, reuse forever (until expiry ~1 month)
- **Privacy** — cookies stored locally with 600 permission

## Requirements

- Python 3.9+
- No external packages
- Bilibili account (logged in via browser to get cookies)

## License

MIT
