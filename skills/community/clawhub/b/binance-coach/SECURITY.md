# Security & Privacy

## Is this safe to install?

Yes — BinanceCoach is a read-only Binance portfolio analyzer. It cannot trade or move funds under any circumstances.

- ✅ **Read-only API access** — the Binance API key it requests physically cannot trade or withdraw
- ✅ **Open source** — every line is auditable at [github.com/UnrealBNB/BinanceCoachAI](https://github.com/UnrealBNB/BinanceCoachAI)
- ✅ **Secrets stay local** — your API keys are written to `~/workspace/binance-coach/.env` on your own machine only, never transmitted to any third party
- ✅ **No always-on privilege** — the skill only runs when you ask it to

---

## What credentials does it need?

| Credential | Why | Required? |
|---|---|---|
| `BINANCE_API_KEY` + `BINANCE_API_SECRET` | Read your portfolio and trade history | ✅ Yes |
| `ANTHROPIC_API_KEY` | Standalone AI coaching without OpenClaw | ❌ Optional |
| `TELEGRAM_BOT_TOKEN` + `TELEGRAM_USER_ID` | Standalone Telegram bot | ❌ Optional |

**How to create safe Binance keys:**
1. binance.com → Account → API Management → Create API
2. Enable **only "Enable Reading"** — nothing else
3. Optionally restrict to your IP for extra safety

A read-only key cannot trade or withdraw even if leaked.

---

## What does setup.sh actually do?

1. **Copies bundled source** from inside this skill package to `~/workspace/binance-coach/` — no internet required, no external code fetched
2. Runs `pip install -r requirements.txt` — standard packages only (python-binance, anthropic, rich, python-dotenv, requests, python-telegram-bot)
3. Writes your API keys to `~/workspace/binance-coach/.env`
4. Verifies Binance connectivity

All source code ships inside this skill and is auditable before running. Full source also on GitHub: [github.com/UnrealBNB/BinanceCoachAI](https://github.com/UnrealBNB/BinanceCoachAI)

---

## What data is stored locally?

- `~/workspace/binance-coach/.env` — your API keys (gitignored, local only)
- `~/workspace/binance-coach/data/behavior.db` — your trade history for behavioral analysis (local SQLite, never leaves your machine)
