---
name: moon-dev-trading-agents
description: Master Moon Dev's AI Agents GitHub with 48+ specialized agents, multi-exchange support, LLM abstraction, and autonomous trading capabilities across crypto markets
---

# Moon Dev's AI Trading Agents System

A complete skillset reference for working with Moon Dev's experimental AI trading architecture — featuring 48+ specialized agents orchestrated across Hyperliquid, Solana (BirdEye), Asterdex, and Extended Exchange.

---

## Instructions

When working with Moon Dev's trading system, use this skill to:

1. **Understand the system architecture**: Reference the core components, agent structure, and data flow patterns described in this skill
2. **Run agents**: Use the quick start commands and workflow examples to execute agents individually or via the orchestrator
3. **Configure exchanges**: Follow the exchange switching patterns to work with Hyperliquid, BirdEye, or Extended Exchange
4. **Switch AI models**: Use ModelFactory patterns to select appropriate LLM providers for different tasks
5. **Develop new agents**: Follow the agent template and development rules when creating new agents
6. **Run backtests**: Use the RBI agent workflow to generate and execute backtests from videos, PDFs, or text descriptions
7. **Debug issues**: Reference the architecture documentation and common workflows to troubleshoot problems

When users ask about agents, trading workflows, exchange configuration, or system architecture, provide guidance based on the comprehensive information in this skill and referenced files (AGENTS.md, WORKFLOWS.md, ARCHITECTURE.md).

---

## 📌 When to Use This Skill

Use this doc when you need to:

- Understand the multi-agent architecture
- Run, modify, or build new agents
- Configure exchanges or LLM providers
- Debug agent interactions
- Run backtests using the RBI agent
- Add new strategies or integrate new exchanges

---

## 🧪 Environment Setup

Uses **Python 3.10.9**.

- Conda, venv, or plain pip — all fine  
- README uses `tflow` as env name, but you can name your env anything

---

## 🚀 Quick Start

```bash
# Activate environment
conda activate tflow
# or
source venv/bin/activate

# Run main orchestrator
python src/main.py

# Run an individual agent
python src/agents/trading_agent.py
python src/agents/risk_agent.py
python src/agents/rbi_agent.py

# After installing new packages
pip freeze > requirements.txt
```

---

## 🏗️ Core Architecture

### Directory Tree

```
src/
├── agents/                 # 48+ specialized AI agents (<800 lines each)
├── models/                 # LLM provider abstraction (ModelFactory)
├── strategies/             # User-defined trading logic
├── scripts/                # Utility scripts
├── data/                   # Saved results, memory, logs
├── config.py               # Global configuration
├── main.py                 # Main orchestrator
├── nice_funcs.py           # Solana/BirdEye utilities
├── nice_funcs_hl.py        # Hyperliquid utilities
├── nice_funcs_extended.py  # Extended Exchange utilities
└── ezbot.py                # Legacy bot
```

### Key Components

#### Agents

Standalone executables with ModelFactory support.
Output saved into `src/data/<agent_name>/`.

#### LLM Providers

Supports: Claude, GPT-4, DeepSeek, Groq, Gemini, Ollama.

```python
from src.models.model_factory import ModelFactory
model = ModelFactory.create_model('anthropic')
```

#### Trading Utilities

* **nice_funcs.py** — Solana/BirdEye
* **nice_funcs_hl.py** — Hyperliquid perps
* **nice_funcs_extended.py** — X10 StarkNet perps

#### Config

* Trading settings
* Risk limits
* Active agents
* AI model configs

---

## 🤖 Agent Categories

### Trading Agents

`trading_agent`, `strategy_agent`, `risk_agent`, `copybot_agent`

### Market Analytics

`sentiment_agent`, `whale_agent`, `funding_agent`, `liquidation_agent`, `chartanalysis_agent`

### Content Bots

`chat_agent`, `tweet_agent`, `clips_agent`, `phone_agent`, `video_agent`

### Research / Backtesting

`rbi_agent`, `research_agent`, `websearch_agent`

### Specialized

`sniper_agent`, `million_agent`, `solana_agent`, `tx_agent`, `polymarket_agent`, `swarm_agent`

---

## 🔄 Common Workflows

### 1. Run any agent

```bash
python src/agents/[agent_name].py
```

### 2. Run orchestrator

```bash
python src/main.py
```

Controlled by `ACTIVE_AGENTS` in `main.py`.

### 3. Switch Exchange

```python
EXCHANGE = "hyperliquid"  # or "birdeye", "extended"

if EXCHANGE == "hyperliquid":
    from src import nice_funcs_hl as nf
elif EXCHANGE == "extended":
    from src import nice_funcs_extended as nf
```

### 4. Switch AI Model

```python
AI_MODEL = "claude-3-haiku-20240307"
```

Or per-agent:

```python
model = ModelFactory.create_model('deepseek')
```

### 5. Backtesting (RBI Agent)

```bash
python src/agents/rbi_agent.py
```

Supports:

* YouTube videos
* PDFs
* Plain text trading ideas

Outputs fully executable Backtesting.py code.

---

## 🧩 Development Rules (Critical)

1. **Files under 800 lines max**
2. **Don't move files** — only create new ones
3. **Use existing virtual environment**
4. Run `pip freeze > requirements.txt` after installs
5. Use **real data only**
6. Minimal try/except — let errors show
7. Never expose API keys

### New Agent Template

```python
from src.models.model_factory import ModelFactory
model = ModelFactory.create_model('anthropic')

output_dir = "src/data/my_agent/"

if __name__ == "__main__":
    # main logic
```

---

## 📊 Backtesting Rules

* Use `backtesting.py` (official library)
* Use `pandas_ta` or `talib` for indicators
* Example dataset: `src/data/rbi/BTC-USD-15m.csv`

---

## ⚙️ Config Files

### `config.py`

* Tokens, whitelists/blacklists
* Position sizing
* Risk settings
* Active agents
* AI model / temperature / max tokens

### `.env`

Contains:

* BirdEye, MoonDev, Coingecko
* Anthropic, OpenAI, DeepSeek, Groq, Gemini
* Solana private keys
* Hyperliquid EVM PK
* X10 API keys

(These must **never** be shown publicly.)

---

## 🏦 Exchange Support

### Hyperliquid

(Perps DEX, 50× leverage)

Functions:

* `market_buy()`
* `market_sell()`
* `get_position()`
* `close_position()`

### BirdEye / Solana

15k+ tokens

* `token_overview()`
* `token_price()`
* `get_ohlcv_data()`

### Extended Exchange (X10)

StarkNet perps
Auto symbol mapping (e.g., BTC → BTC-USD).

---

## 🔁 Data Flow

```
Input + Config
→ Agent Init
→ API Calls
→ Data Parsing
→ LLM Reasoning
→ Decision Output
→ Save to data/
→ (optional) Execute Trade
```

---

## 🧪 Common Tasks

### Install new package

```bash
pip install package-name
pip freeze > requirements.txt
```

### Read market data

```python
from src.nice_funcs import token_overview, get_ohlcv_data, token_price
```

### Hyperliquid trade

```python
from src import nice_funcs_hl as nf
nf.market_buy("BTC", usd_amount=100, leverage=10)
```

### X10 trade

```python
from src import nice_funcs_extended as nf
nf.market_buy("BTC", usd_amount=100, leverage=15)
```

---

## 🧵 Git Information

* **Branch:** main

Recent commits:

* `dc55e90`: websearch agent
* `921ead6`: rbi update
* `6bb55c2`: backtest dashboard

---

## 📚 Documentation

Located in `docs/`:

* hyperliquid.md
* extended_exchange.md
* rbi_agent.md
* swarm_agent.md
* claude.md
* websearch_agent.md
* etc.

---

## 🛡️ Risk Management

* Risk Agent runs **first**
* Circuit breakers:

  * MAX_LOSS_USD
  * MINIMUM_BALANCE_USD
* AI-confirmation optional for closing trades
* Default loop: every **15 min**

---

## 🧠 Philosophy

This project is experimental, community-driven, educational, and open-source.
No token. No promises. No nonsense.

> "Never over-engineer. Always ship real trading systems."

---

**Built with 🌙 by Moon Dev**
