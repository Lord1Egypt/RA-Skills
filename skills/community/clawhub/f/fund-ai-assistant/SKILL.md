---
name: fund-ai-assistant
display_name: Fund AI Assistant
description: Fund portfolio tracker with AI analysis, multi-agent debate, technical indicators (VaR/Sortino/Calmar), macro monitoring, and rebalancing alerts.
---

# Fund AI Assistant

**Version**: 3.0 | **License**: MIT-0 | **LLM**: Any OpenAI-compatible provider

---

## Overview

A local-first fund investment assistant running entirely on your machine. Fetches data from East Money, analyzes with any LLM provider, and supports scheduled tasks via OpenClaw or crontab.

> ⚠️ **Security Notice**: This skill requires `LLM_MODEL` + `LLM_API_KEY`. Use a dedicated API key. See Section 7 for all security considerations.

---

## 1. Features

| Feature | Description |
|---------|-------------|
| 📊 Technical Analysis | MACD / KDJ / RSI / Bollinger Bands / MA + **VaR / Sortino / Calmar** |
| 🤖 AI Quantitative Analysis | Any LLM (OpenAI-compatible), outputs buy/sell/hold with price targets |
| ⚖️ Multi-Agent Debate | 6 roles → game-theory judge verdict |
| 📋 Portfolio Rebalancing | Detects allocation drift, outputs precise rebalancing instructions |
| 🎯 Entry Timing | RSI + Bollinger + trend composite score |
| 🌡️ Correlation Heatmap | Pairwise correlation matrix for diversification |
| 🌍 Macro Event Monitor | CSI300 / USD-CNY / FOMC / LPR alerts |

---

## 2. Environment Variables

### Required

| Variable | Description |
|----------|-------------|
| `LLM_MODEL` | Model name, e.g. `gpt-4o-mini` |
| `LLM_API_KEY` | Your LLM API key |

### Optional

| Variable | Description |
|----------|-------------|
| `LLM_API_BASE` | ⚠️ Custom API URL — if untrusted, your key and data go there. Use endpoints you control. Default: `https://api.openai.com/v1` |
| `TAVILY_API_KEY` | Tavily API for real-time macro search |
| `FUND_SCENE_DIR` | Directory with optional `.md` scene templates (default: `./scenes/`) |
| `PUSH_WEBHOOK_URL` | Generic HTTP POST webhook (WeCom / Feishu / Slack) |
| `BARK_PUSH_URL` | iOS Bark notification URL |
| `PUSH_EMAIL` | Target email for SMTP push |
| `SMTP_HOST/PORT/USER/PASS` | SMTP configuration (used with `PUSH_EMAIL`) |
| `QQ_WEBHOOK_URL` | QQ bot HTTP interface (go-cqhttp / Lagrange) |

### Setup Example

```bash
export LLM_MODEL="gpt-4o-mini"
export LLM_API_KEY="sk-xxx"

# Optional
export TAVILY_API_KEY="tvly-xxx"
export PUSH_WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
```

---

## 3. Installation

```bash
# 1. Clone
git clone https://github.com/tempest-01/fund-ai-assistant.git
cd fund-ai-assistant

# 2. Install optional dependencies (charts)
pip install -r requirements.txt

# 3. Configure
cp config.example.json config.json
cp positions.example.json positions.json

# 4. Set environment variables (see Section 2)
export LLM_MODEL="your_model"
export LLM_API_KEY="your_key"

# 5. Verify
python3 analyzer.py list
python3 analyzer.py analyze
```

---

## 4. Script Reference

| Script | Function | Usage |
|--------|----------|-------|
| `analyzer.py` | Main entry, tracking + analysis | `python3 analyzer.py list` |
| `ai_analysis.py` | AI quantitative analysis | `python3 ai_analysis.py` |
| `debate_analyzer.py` | Multi-agent debate | `python3 debate_analyzer.py <code>` |
| `rebalance.py` | Portfolio drift detection | `python3 rebalance.py` |
| `recommend.py` | Entry timing suggestions | `python3 recommend.py` |
| `event_monitor.py` | Macro event monitor | `python3 event_monitor.py` |
| `correlation_v2.py` | Correlation heatmap | `python3 correlation_v2.py` |
| `fund_api.py` | East Money data API | `python3 fund_api.py` |
| `technical.py` | Technical indicators | `python3 technical.py` |
| `chart_generator.py` | PIL chart generation | `python3 chart_generator.py` |
| `positions.py` | Position record management | `python3 positions.py` |
| `macro_fetcher.py` | Macro data fetcher | `python3 macro_fetcher.py` |
| `strip_color.py` | ANSI strip for cron | `cmd \| python3 strip_color.py` |
| `llm.py` | Unified LLM interface | `from llm import get_llm_config, call_llm` |

---

## 5. Scheduled Tasks (Reference)

```bash
# OpenClaw users
openclaw cron add --cron "0 8 * * 1-5" \
  --message "cd /path/to/fund-ai-assistant && python3 event_monitor.py --dry-run"

openclaw cron add --cron "30 9 * * 1-5" \
  --message "cd /path/to/fund-ai-assistant && python3 analyzer.py analyze"

# crontab users
0 8 * * 1-5 cd /path/to/fund-ai-assistant && python3 event_monitor.py >> /var/log/fund.log 2>&1
```

---

## 6. File Structure

```
fund-ai-assistant/
├── .gitignore
├── _meta.json              # Registry metadata
├── SKILL.md               # This file
├── README.md              # Full bilingual documentation
├── config.example.json     # Tracking list template
├── positions.example.json  # Position record template
├── requirements.txt       # Optional: Pillow / numpy / matplotlib
├── llm.py                # Unified LLM interface
├── analyzer.py            # Main entry
├── ai_analysis.py         # AI quantitative analysis
├── debate_analyzer.py    # Multi-agent debate
├── rebalance.py           # Portfolio drift detection
├── recommend.py          # Entry timing
├── event_monitor.py      # Macro event monitor
├── correlation_v2.py     # Correlation heatmap
├── fund_api.py           # East Money API
├── technical.py          # Technical indicators
├── chart_generator.py    # PIL chart generation
├── macro_fetcher.py      # Macro data
├── positions.py          # Position records
├── strip_color.py        # ANSI color strip
└── assets/             # Chart output (auto-created)
```

---

## 7. Security Notes

**Read carefully before installing and running.**

### Required Credentials

- `LLM_MODEL` and `LLM_API_KEY` are **required**. Use a dedicated API key, not a high-value production key.
- Before first run, inspect `llm.py` and `fund_api.py` to confirm no credential exfiltration.

### Filesystem Access

- `FUND_SCENE_DIR`: The skill reads `.md` template files from the directory you specify.
  - **Do NOT** point it at system directories, home directories, or folders containing secrets.
  - If unset, defaults to `{skill_dir}/scenes/` (which is created empty).
  - Only `.md` files in that directory are read.

### Network Access

- **East Money APIs**: `fundgz.1234567.com.cn`, `api.fund.eastmoney.com` — public fund data.
- **Tavily** (if `TAVILY_API_KEY` set): Real-time macro search.
- **Push endpoints** (if configured): Analysis summaries are sent to the URLs you provide.

### Push Channels

If any of these are set, analysis output will be transmitted externally:

| Variable | Transmission |
|----------|-------------|
| `PUSH_WEBHOOK_URL` | HTTP POST to your webhook URL |
| `BARK_PUSH_URL` | GET request to your Bark URL |
| `PUSH_EMAIL` | SMTP email to your address |
| `QQ_WEBHOOK_URL` | HTTP POST to your QQ bot |

> Use endpoints you control. Do not set these with untrusted third-party URLs.

### Data Privacy

- All fund data is fetched from East Money on demand; no persistent storage of market data.
- Position records (`positions.json`) are stored locally in the skill directory only.
- LLM API key is sent only to the configured `LLM_API_BASE` endpoint.
- No telemetry, no external analytics, no data sent to third parties without explicit configuration.

### Recommended Precautions

1. **Use a dedicated LLM API key** — not your main production key.
2. **⚠️ Inspect `LLM_API_BASE`** — if set to an untrusted endpoint, your API key and fund data will be sent there. Only use `https://api.openai.com/v1` or endpoints you control.
3. **Review `llm.py` and `fund_api.py`** before first run.
4. **Run in an isolated environment** (container or VM) on first use.
5. **Do not set `FUND_SCENE_DIR`** to sensitive directories.
6. **Do not share your `LLM_API_KEY`** or push endpoint URLs.

---

## 8. Inspiration & Attribution

- **[astrbot_plugin_fund_analyzer](https://github.com/2529huang/astrbot_plugin_fund_analyzer)** — Multi-agent debate framework inspiration; adapted from stock to fund analysis with added portfolio management features.
- **[OpenClaw](https://github.com/openclaw/openclaw)** — Scheduling and notification infrastructure.
- **East Money (东方财富)** — Fund price and history data source.
- **Tencent Finance (腾讯财经)** — CSI300 real-time data source.

---

*This skill was developed with AI assistance.*
