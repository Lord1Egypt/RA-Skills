# BinanceCoach — Full Command Reference

## CLI Commands (via `scripts/bc.sh`)

### Portfolio Analysis
```bash
bc.sh portfolio
```
Returns: health score (0-100), grade (A-F), total USD, top holdings with %, stablecoin %, suggestions.

### Smart DCA Recommendations
```bash
bc.sh dca                              # Default: BTC, ETH, BNB
bc.sh dca DOGEUSDT ADAUSDT BNBUSDT     # Custom symbols
```
Returns: per-coin multiplier, weekly buy amount, rationale (RSI + F&G + SMA200 context).

Multiplier logic (RSI zone × Fear & Greed zone, 25 combinations):
- Oversold + Extreme Fear → ×2.0 (max buy)
- Overbought + Extreme Greed → ×0.2 (min buy)
- Base = monthly_budget / 4 weeks × risk_modifier

### Market Context
```bash
bc.sh market BTCUSDT                   # Default: BTCUSDT
bc.sh market DOGEUSDT
```
Returns: price, RSI (+ zone), trend (strong_up/recovering/downtrend/mixed), SMA50, SMA200, EMA21, vs SMA200 %, Fear & Greed.

### Fear & Greed Index
```bash
bc.sh fg
```
Returns: score (0-100), classification, buy/hold/sell advice.

### Behavioral Analysis
```bash
bc.sh behavior
```
Returns:
- FOMO Score (0-100): based on F&G extremes + rapid buy clusters
- Overtrading Index: trades/week (Healthy < 5/week, Moderate < 15, High < 30, Overtrader 30+)
- Panic Sell Detector: sells where price recovered 15%+ since
- Streaks: days without panic sell, DCA consistency weeks

### Alerts
```bash
bc.sh alert BTCUSDT above 70000        # Price above
bc.sh alert BTCUSDT below 50000        # Price below
bc.sh alert BTCUSDT rsi_above 70       # RSI overbought alert
bc.sh alert BTCUSDT rsi_below 30       # RSI oversold alert
bc.sh alerts                           # List active alerts
bc.sh check-alerts                     # Manually check if any triggered
```

### Education
```bash
bc.sh learn                            # List all 7 lessons
bc.sh learn rsi_oversold
bc.sh learn rsi_overbought
bc.sh learn fear_greed
bc.sh learn dca
bc.sh learn sma_200
bc.sh learn concentration_risk
bc.sh learn panic_selling
```

### DCA Projection
```bash
bc.sh project BTCUSDT                  # 12-month projection
```
Returns: total invested, projected value (5% avg monthly growth), ROI %.

### AI Coaching (Claude)
```bash
bc.sh coach                            # Full AI portfolio coaching summary
bc.sh weekly                           # Weekly behavior + action plan brief
bc.sh ask "should I sell all my DOGE?" # Free-form question with live portfolio context
bc.sh models                           # List available Claude models
bc.sh model claude-sonnet-4-6          # Switch active model
```

**`ask` auto-enrichment**: Detects coin symbols in the question and fetches live market data for each. Always includes full portfolio, holdings, behavioral analysis, and Fear & Greed. Claude never has to ask "what's your portfolio?" — it already knows.

### News & Announcements
```bash
bc.sh news                             # Latest 5 Binance news/announcements
bc.sh news 10                          # Latest 10 items
bc.sh listings                         # New coin listings (last 5)
bc.sh listings 10                      # New coin listings (last 10)
bc.sh launchpool                       # Active launchpools & HODLer airdrops
bc.sh news-check                       # Only show NEW unseen items (deduped, heartbeat use)
```

Returns: article title, date, and clickable URL. Portfolio cross-reference: flags if a listed coin matches your holdings.

### Real-time Watcher
```bash
bc.sh watch                            # Poll every 60s, notify Telegram on new items (foreground)
bc.sh watch 30                         # Poll every 30s
bc.sh watch-bg                         # Same but runs in background (nohup, survives logout)
bc.sh watch-bg 30                      # Background watcher at 30s interval
bc.sh watch-stop                       # Stop the running background watcher
bc.sh watch-status                     # Check if watcher is running + PID
```

Requirements: `TELEGRAM_BOT_TOKEN` and `TELEGRAM_USER_ID` must be set in `.env`.

### Bot Modes
```bash
bc.sh telegram                         # Start Telegram bot (persistent, polls news every 2 min)
bc.sh demo                             # Demo mode (no Binance API keys needed)
```

---

## Telegram Bot Commands

Same functionality via Telegram. All 21 commands:

| Command | Description |
|---|---|
| `/start` | Show help menu |
| `/portfolio` | Portfolio health analysis |
| `/dca [SYMBOLS]` | Smart DCA recommendations |
| `/market [SYM]` | Market context |
| `/fg` | Fear & Greed index |
| `/alert SYM COND VALUE` | Set price/RSI alert |
| `/alerts` | List active alerts |
| `/checkalerts` | Check triggered alerts |
| `/behavior` | Behavioral analysis |
| `/project [SYM]` | 12-month DCA projection |
| `/learn [TOPIC]` | Educational lessons |
| `/coach` | AI coaching summary |
| `/weekly` | Weekly AI brief |
| `/ask <question>` | Ask Claude anything |
| `/models` | List Claude models |
| `/model <id>` | Switch Claude model |
| `/lang` | Change language (inline buttons) |
| `/news` | Latest Binance news & announcements |
| `/listings` | New coin listings |
| `/launchpool` | Active launchpools & HODLer airdrops |
| `/watchstatus` | Check if background watcher is running |

**Auto-notifications (Telegram bot only):**
- **Alerts:** checked every 5 minutes, pushed automatically when triggered
- **News/listings/launchpools:** checked every **2 minutes**, pushed automatically when new items appear — no command needed

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `BINANCE_API_KEY` | — | Binance read-only API key |
| `BINANCE_API_SECRET` | — | Binance read-only secret |
| `ANTHROPIC_API_KEY` | — | Claude API key |
| `AI_MODEL` | `claude-haiku-4-5-20251001` | Active Claude model |
| `TELEGRAM_BOT_TOKEN` | — | Telegram bot token |
| `TELEGRAM_USER_ID` | — | Authorized Telegram user ID |
| `LANGUAGE` | `en` | `en` or `nl` |
| `RISK_PROFILE` | `moderate` | `conservative` / `moderate` / `aggressive` |
| `DCA_BUDGET_MONTHLY` | `500` | Monthly DCA budget (USD) |
| `BINANCE_COACH_PATH` | — | Override project location |
