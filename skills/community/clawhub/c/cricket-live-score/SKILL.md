---
name: cricket-live-score
description: Send live cricket score updates (text + voice memo) to Telegram for any ongoing T20 or ODI match. Completely free. 
author: Amit Kulkarni
tags: cricket, sports, live-score, telegram, voice
dependencies: gTTS
env: TELEGRAM_BOT_TOKEN (optional — can also use --bot-token arg or OpenClaw config)
config: ~/.openclaw/openclaw.json (optional fallback for bot token)
---

# 🏏 Cricket Live Score Updates

Real-time cricket score updates delivered to Telegram — with optional voice memos so you can follow along without reading. Scrapes data from cricbuzz and does not need any API key setup to get the scores. 

Supports T20 and ODI formats, both innings, auto-detection of teams, target, and required run rate.

The script runs in the background, sends updates at your chosen interval, and auto-stops when the match ends.

The voice memos are perfect for when you're driving or otherwise can't focus on a screen.

## Example prompts

**Starting updates:**
- "Send me live score updates for the India vs Australia match"
- "Follow the IPL match — RCB vs CSK — and send me updates every 3 minutes"
- "What's the score in the England vs Pakistan T20? Keep me posted"

**With voice memos:**
- "Send me live cricket scores with voice memos for the World Cup final"
- "Follow India vs South Africa and include voice updates — I'm driving"

**Changing interval:**
- "Make the updates every 2 minutes instead"
- "Slow it down to every 10 minutes"

**Stopping:**
- "Stop sending score updates"
- "Kill the cricket updates"

## When to use

User asks for live score updates, cricket score alerts, or to follow a match.

## How it works

1. **Find the Cricbuzz URL** for the match. Search for `cricbuzz <team1> vs <team2> live score` and grab the `cricbuzz.com/live-cricket-scores/...` URL.
2. **Run the script** in background:

```bash
python3 <skill_dir>/scripts/cricket-live.py \
  --url "<cricbuzz_url>" \
  --chat-id "<telegram_chat_id>" \
  --bot-token "<telegram_bot_token>" \
  --interval 300 \
  --voice
```

3. Script auto-detects teams, innings, format (T20/ODI), and target.
4. Sends text + voice memo every interval. Auto-stops when match ends.

## Parameters

| Param | Default | Description |
|-------|---------|-------------|
| `--url` | required | Cricbuzz live score page URL |
| `--chat-id` | required | Telegram chat ID to send updates to |
| `--bot-token` | auto | Telegram bot token. Falls back to `TELEGRAM_BOT_TOKEN` env var, then OpenClaw config (`~/.openclaw/openclaw.json`) |
| `--interval` | 300 | Seconds between updates (default 5 min) |
| `--voice` | off | Include voice memo with each update |

## What the updates look like

### 2nd innings (chase)
```
*India: 146/4 (15 ov)*
  🏏 Tilak Varma — 20 (15)
  🏏 Sanju Samson — 80 (40)

Need: 50 runs off 30 balls
RRR: 10.0 per over with 5.0 overs to go
Last wicket: Suryakumar Yadav c Rutherford b Joseph 18 (16)

🔹 WI innings: 195/4 (20 ov)
━━━━━━━━━━━━━━━━━
🏏 IND vs WI | ICC Men's T20 World Cup 2026

· Next update in 5 min
```

### 1st innings
```
*West Indies: 120/3 (15 ov)*
  🏏 Rovman Powell — 25 (14)
  🏏 Jason Holder — 12 (8)

Run rate: 8.0 per over
Projected: 160
Last wicket: Shimron Hetmyer c Samson b Bumrah 22 (18)

━━━━━━━━━━━━━━━━━
🏏 IND vs WI | ICC Men's T20 World Cup 2026

· Next update in 5 min
```

### Voice memo examples

**2nd innings:** "India are 146 for 4 in 15 overs. Tilak Varma and Sanju Samson are batting. Tilak Varma is on 20, and Sanju Samson is on 80. India need 50 runs off 30 balls. Required run rate is 10.0 per over, with 5.0 overs to go."

**1st innings:** "West Indies are 120 for 3 in 15 overs. Rovman Powell and Jason Holder are batting. Run rate is 8.0 per over. Projected total is 160."

## Data source

Scrapes Cricbuzz — the `og:description` meta tag for live scores and batsmen, plus embedded JSON for last wicket, bowler stats, and team info. No paid API or API key required for score data.

## Stopping

- Script auto-stops when it detects a match result (won/tied/no result).
- To stop manually, kill the background process.

## Channel support

Currently **Telegram only** — the script sends updates directly via the Telegram Bot API. Multi-channel support (Discord, WhatsApp, Signal, etc.) is planned for a future version.

## Requirements

- Python 3 (uses only `urllib` from the standard library — no `requests` needed)
- `gTTS` package (for voice memos)
- Telegram bot token — provided via one of:
  1. `--bot-token` argument (recommended)
  2. `TELEGRAM_BOT_TOKEN` environment variable
  3. OpenClaw config file (`~/.openclaw/openclaw.json` → `channels.telegram.botToken`)

## Known limitations

- When the chasing team is all out or completes their overs without reaching the target, the script may be slow to detect the result (depends on Cricbuzz updating the page title). It reliably catches wins, ties, and target-reached scenarios.
