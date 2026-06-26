**English** | [中文](README.zh-CN.md)

# FirstKnow

**Your stocks just made news. You're the first to know what it means.**

An AI-powered portfolio intelligence agent that monitors breaking news, SEC filings,
price moves, and analyst actions for stocks you hold — and pushes personalized alerts
straight to your Telegram. 24/7. In your language.

## What You Get

A Telegram alert within minutes of news breaking:

```
🔔 Morgan Stanley Maintains Overweight on NVIDIA, Raises Price Target to $1,100

📌 Your holding: NVDA (20% of portfolio)
📈 Analyst Rating | NVDA +1.8% | $892

📰 Morgan Stanley analyst Joseph Moore maintains NVIDIA (NASDAQ:NVDA)
with an Overweight rating and raises the price target from $960 to
$1,100, citing continued AI data center demand acceleration.

🔗 https://finnhub.io/api/news?id=12345

💬 Reply "deep" for AI-powered analysis
```

Reply "deep" for a full portfolio-aware analysis:

```
📊 NVDA Analyst Upgrade — Deep Analysis

What's really going on:
This is the 5th major analyst PT raise in 2 months. Morgan Stanley's
new $1,100 target implies 23% upside from current price...

Historical precedent:
Last time 3+ analysts raised PT in the same week (Jan 2026), NVDA
rallied 12% over the following 3 weeks...

Stress test:
• Best case (30%): AI capex cycle extends through 2027 → $1,200+
• Base case (50%): Current trajectory holds → $950-1,050 range
• Worst case (20%): Demand pull-forward concerns → $780-850

Action items:
• Hold current 20% position — no action needed now
• If drops below $840: add 3% (bring to 23%)
• Set trailing stop at $810 for downside protection

📌 Watch: NVDA Q1 earnings May 28, AMD earnings May 6
```

## Installation

### OpenClaw (via ClawHub)

```bash
clawhub install firstknow
```

Then message your OpenClaw agent (via Telegram, Feishu, Discord, etc.):
"set up firstknow"

### OpenClaw (manual)

```bash
git clone https://github.com/cdpiano/firstknow.git ~/.claude/skills/firstknow
cd ~/.claude/skills/firstknow/scripts && npm install
```

### Claude Code

```bash
git clone https://github.com/cdpiano/firstknow.git ~/.claude/skills/firstknow
cd ~/.claude/skills/firstknow/scripts && npm install
```

Then in Claude Code, say "set up firstknow" or invoke `/firstknow`.

### Update

```bash
cd ~/.claude/skills/firstknow && git pull
```

## Quick Start

After installation, just tell your agent "set up firstknow". It walks you through
everything conversationally — no config files to edit.

The agent will ask you:
- What you hold (e.g. "NVDA 25%, BTC 20%, TSLA 15%")
- Language preference (English / Chinese / Bilingual)
- Alert level (all events / major only / daily digest)
- Quiet hours
- Telegram bot setup (guided step by step)

**That's it.** Basic alerts start arriving within 5 minutes.

## News Sources

Your alerts are powered by 4 real-time data sources:

| Source | Covers | Examples |
|--------|--------|---------|
| **Finnhub** | Stock news | Reuters, Benzinga, MarketWatch articles |
| **SEC EDGAR** | Regulatory filings | 10-K, 10-Q, 8-K, insider trades, activist stakes |
| **Yahoo Finance** | Price moves | Detects daily moves > 5% |
| **CoinGecko** | Crypto prices | BTC, ETH, SOL and 15+ other tokens |

All data fetching happens on a centralized backend. No API keys needed from you
for basic alerts.

## Deep Analysis

Reply "deep" (or "深度") to any alert for a full AI-powered analysis that includes:

- What's really going on beneath the headline
- Historical precedent (similar events and how the stock reacted)
- Portfolio stress test (best/base/worst case scenarios)
- Specific action items ("if drops below $780, add 3%")
- Key dates and indicators to watch

Deep analysis uses Claude Sonnet and requires your own Anthropic API key (asked during setup).

## Changing Settings

Everything is configurable through conversation:

- "Switch to Chinese" / "切换中文"
- "Only send me major events"
- "Change quiet hours to 11pm-7am"
- "I sold TSLA and bought GOOGL 15%"
- "Show my settings"
- "Show my portfolio"

## How It Works

```
Backend (24/7)                        Skill (your agent)
+---------------------------+         +------------------------+
| Fetches news every 5 min  |         | Onboarding             |
| Monitors SEC filings      |         | Deep analysis (Claude) |
| Detects price anomalies   |  API    | Portfolio updates       |
| Matches to YOUR holdings  | <-----> | Settings changes        |
| Translates (if needed)    |         |                        |
| Pushes to YOUR Telegram   |         |                        |
+---------------------------+         +------------------------+
     Always running                     Runs when you need it
```

**Basic alerts work 24/7** — even when your computer is off, even when your agent
isn't running. The backend handles everything.

**Deep analysis** runs on-demand through your agent when you reply "deep" to an alert.

## Anti-Spam

Built-in protections so you don't get overwhelmed:

- Max 3 alerts per ticker per day
- 30-minute cooldown between same-ticker alerts
- Quiet hours (configurable, default 12am-8am)
- Alert level filter (all / major / digest)

## Language Support

| Setting | What happens |
|---------|-------------|
| English | All alerts in English |
| 中文 | Headlines and summaries auto-translated to Chinese |
| Bilingual | English + Chinese in every alert |

Translation happens server-side. No extra cost or setup for you.

## Privacy

- Your portfolio is stored on the backend to match news events. Not shared with third parties.
- News APIs only receive ticker symbols, never personal information.
- You can delete all your data anytime by telling the agent "delete my account."

## Requirements

- A Telegram account (for receiving alerts)
- An Anthropic API key (only for deep analysis — basic alerts are free)
- OpenClaw or Claude Code (for running the skill)

## License

MIT
