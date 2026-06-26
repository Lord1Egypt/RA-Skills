# BinanceCoach — Agent Guide (OpenClaw Internal)

This file contains full dispatch instructions for OpenClaw. Read this when you need to know exactly which command to run for a given user request.

---

## ⚠️ Security Notes for Agents

- **API keys are written directly to `~/workspace/binance-coach/.env` on disk** — never log them in conversation history, never store them in memory files, never include them in tool call output
- **`.env` is gitignored** — it will never be committed to any repo
- **Only read-only Binance keys are needed** — no trading, no withdrawal permissions ever
- **In OpenClaw mode, no Anthropic key is needed** — OpenClaw IS Claude. Do not ask for or store an Anthropic API key
- When writing `.env`, use the `write` tool directly — do not echo secrets to terminal output

---

## Scheduled Analysis Crons

BinanceCoach sends daily portfolio analysis via two OpenClaw crons — morning (09:00) and evening (21:00). These must be created with `agentTurn` payload + `isolated` session + `announce` delivery to actually reach the user on Telegram. Using `systemEvent` with `main` session will silently run but never deliver.

**Correct cron config:**
```bash
openclaw cron add \
  --name "BinanceCoach Morning Analysis" \
  --cron "0 9 * * *" \
  --tz "Europe/Amsterdam" \
  --session isolated \
  --message "Run the BinanceCoach morning portfolio analysis: cd ~/workspace/binance-coach && python3 scripts/daily_analysis.py — then send the complete output to the user on Telegram." \
  --announce \
  --to "telegram:<USER_TELEGRAM_ID>"
```

**If a user says they're not receiving analysis reports:**
1. Check crons: `openclaw cron list` — look for `sessionTarget: main` or `payload.kind: systemEvent` on BinanceCoach jobs → those are broken
2. Fix with: `bc.sh setup-crons`
3. Or manually edit: `openclaw cron edit <id> --session isolated --message "<text>" --announce --to "telegram:<id>"`

**To set up crons for a new install:**
```bash
bc.sh setup-crons
```
This is also offered as an optional step during `bc.sh setup`.

---

## Updating BinanceCoach

When a user says "update BinanceCoach", "upgrade the skill", or "get the latest version":

1. First show what's changing:
```bash
clawhub info binance-coach 2>/dev/null || echo "Check https://clawhub.ai/skills/binance-coach for latest changelog"
```

2. Then update (preserves .env and data/):
```bash
scripts/bc.sh update
```

This does three things:
1. `clawhub update binance-coach` — pulls latest skill files from ClaWHub
2. Copies new bundled `src/` to `~/workspace/binance-coach/` — preserves `.env` and `data/alerts.db`
3. Re-runs `pip install` in case dependencies changed

The user's API keys and alert history are **never touched**.

---

## Setup Check (always do this first)

```bash
ls ~/workspace/binance-coach/.env 2>/dev/null || echo "NOT CONFIGURED"
```

If not configured → follow the setup flow below.

---

## Setup Flow

**Step 1 — Copy bundled source**
```bash
SKILL_DIR="/path/to/skills/binance-coach"
mkdir -p ~/workspace/binance-coach/data
cp -r "$SKILL_DIR/src/." ~/workspace/binance-coach/
pip3 install --break-system-packages -q -r ~/workspace/binance-coach/requirements.txt
```

**Step 2 — Ask for Binance API keys (required)**
> "Go to binance.com → Account → API Management → Create API with **Read Only** permissions only. Paste your API Key and Secret here."

Write to `.env` using the `write` tool (not echo/terminal):
```
BINANCE_API_KEY=<key>
BINANCE_API_SECRET=<secret>
LANGUAGE=en
RISK_PROFILE=moderate
DCA_BUDGET_MONTHLY=500
AI_MODEL=claude-haiku-4-5-20251001
```

**Step 3 — Preferences (optional)**
> "What's your monthly DCA budget in USD? (default: $500) And risk profile: conservative / moderate / aggressive? (default: moderate)"

**Step 4 — Telegram bot (only if explicitly requested)**
> "Create a bot via @BotFather on Telegram: /newbot → copy the token. Get your Telegram user ID from @userinfobot."

Add to `.env`:
```
TELEGRAM_BOT_TOKEN=<token>
TELEGRAM_USER_ID=<your_id>
```
Then start: `scripts/bc.sh telegram`

**Step 5 — Ask user before hooking into USER.md**

After setup is complete, **ask the user** if they want BinanceCoach registered as their default crypto handler. Do NOT write to USER.md without explicit consent.

Say something like:
> "BinanceCoach is ready! Would you like me to set it as your default for all crypto questions? I'll add a preference to your USER.md so every future session uses it automatically — you can remove it anytime."

If they say yes, append to `USER.md` (usually `~/.openclaw/workspace/USER.md`):

```markdown
## BinanceCoach (Auto-installed)

- **Crypto preference:** Always use the BinanceCoach skill for ANY crypto-related question — DCA advice, portfolio analysis, market data, Fear & Greed index, launchpools, new listings, Binance news, trading behavior, alerts, projections, and anything else Binance/crypto related. Never do manual lookups when BinanceCoach can handle it.
- **Watcher:** To get real-time Binance announcement notifications, run `bc.sh watch-bg`
```

Check first: if `USER.md` already contains `BinanceCoach (Auto-installed)`, skip — don't duplicate.

If they say no: skip silently. They can still use BinanceCoach by mentioning it explicitly.

> **Why this matters:** Without this, a fresh session has no memory of BinanceCoach and may do manual API lookups. But the user should always consent before their config files are modified.

---

## .env Template

```env
BINANCE_API_KEY=...
BINANCE_API_SECRET=...
LANGUAGE=en
RISK_PROFILE=moderate
DCA_BUDGET_MONTHLY=500
AI_MODEL=claude-haiku-4-5-20251001
# Optional — standalone Telegram bot only:
TELEGRAM_BOT_TOKEN=...
TELEGRAM_USER_ID=...
```

---

## Command Dispatch Table

Run all commands via:
```bash
bash /path/to/skills/binance-coach/scripts/bc.sh <command>
```

| User asks | Command |
|---|---|
| Portfolio / holdings / health | `bc.sh portfolio` |
| DCA advice (default coins) | `bc.sh dca` |
| DCA for specific coin | `bc.sh dca DOGEUSDT ADAUSDT` |
| Fear & Greed | `bc.sh fg` |
| Market data for coin | `bc.sh market BTCUSDT` |
| Behavior / FOMO / panic sells | `bc.sh behavior` |
| Set price alert | `bc.sh alert BTCUSDT above 70000` |
| Set RSI alert | `bc.sh alert BTCUSDT rsi_below 30` |
| List alerts | `bc.sh alerts` |
| Check alerts | `bc.sh check-alerts` |
| Learn / education | `bc.sh learn dca` |
| 12-month projection | `bc.sh project BTCUSDT` |
| Latest Binance news | `bc.sh news` |
| New coin listings | `bc.sh listings` |
| Launchpool / HODLer airdrops | `bc.sh launchpool` |
| News-check (unseen only, heartbeat) | `bc.sh news-check` |
| Start watcher (foreground) | `bc.sh watch` |
| Start watcher (background, persistent) | `bc.sh watch-bg` |
| Start watcher custom interval | `bc.sh watch-bg 30` |
| Stop watcher | `bc.sh watch-stop` |
| Watcher running? | `bc.sh watch-status` |
| Start Telegram bot | `bc.sh telegram` |
| Demo mode | `bc.sh demo` |
| Update skill | `bc.sh update` |

Available learn topics: `rsi_oversold`, `rsi_overbought`, `fear_greed`, `dca`, `sma_200`, `concentration_risk`, `panic_selling`

---

## AI Coaching in OpenClaw Mode

**In OpenClaw mode, you ARE Claude — do NOT call `bc.sh coach`, `bc.sh weekly`, or `bc.sh ask`.**

Those commands require a standalone `ANTHROPIC_API_KEY` and are only for the Telegram bot (standalone mode). In OpenClaw mode, Claude is already built in.

Instead — fetch data and analyze it yourself:
1. `bc.sh portfolio` → portfolio holdings, health score
2. `bc.sh behavior` → FOMO score, overtrading, panic sells
3. `bc.sh fg` → Fear & Greed index
4. `bc.sh dca` → DCA multipliers and weekly amounts
5. `bc.sh market <SYMBOL>` → price, RSI, SMA200 for specific coins

Then synthesize the output and respond as the coach directly.

---

## News / Listings / Launchpool — Intent Mapping

| User says | Command |
|---|---|
| "latest news", "any announcements", "what's new on Binance" | `bc.sh news` |
| "new listings", "new coins on Binance", "what got listed" | `bc.sh listings` |
| "launchpool", "hodler airdrop", "any airdrops", "staking rewards" | `bc.sh launchpool` |
| "notify me", "watch for announcements", "alert me when something drops", "real-time updates" | `bc.sh watch-bg` (background) |
| "stop watching", "stop the watcher" | `bc.sh watch-stop` |
| "is the watcher running", "watcher status" | `bc.sh watch-status` |

When user asks to be notified/watched: run `bc.sh watch-bg` — this starts the background daemon and tells them Telegram notifications will arrive within ~60 seconds of any new announcement.

## Output Handling

- `portfolio` → summarize score, grade, top holdings, concentration warnings, suggestions
- `dca` → share multiplier (×1.0 / ×1.3 / ×2.0 etc.) and weekly amount per coin, plus reasoning
- `behavior` → highlight FOMO score, overtrading label, panic sells detected
- `fg` → share score, label, and buy/hold/accumulate advice
- `market` → share price, RSI zone, trend, vs SMA200 %
- `news` / `listings` → list titles + dates; mention portfolio cross-reference if any hits
- `launchpool` → list active launchpools/airdrops; flag if user holds BNB (likely eligible)
- `watch-bg` → confirm watcher started, tell user they'll get Telegram pings within 60s of new drops

---

## Updating Config

```bash
sed -i '' 's/^LANGUAGE=.*/LANGUAGE=nl/' ~/workspace/binance-coach/.env
sed -i '' 's/^DCA_BUDGET_MONTHLY=.*/DCA_BUDGET_MONTHLY=750/' ~/workspace/binance-coach/.env
sed -i '' 's/^RISK_PROFILE=.*/RISK_PROFILE=aggressive/' ~/workspace/binance-coach/.env
```

## Language

Set via `.env` or per-command:
```bash
bc.sh --lang nl portfolio
```
