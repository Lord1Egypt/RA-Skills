# 🧠 Skill: Crypto Alpha Daily Agent

## 📌 Overview
Crypto Alpha Daily Agent is an AI-powered automation system designed to collect, analyze, and generate daily crypto news insights.

This agent is ideal for:
- Crypto content creators
- Traders & investors
- Web3 automation systems
- Social media bots (X / Telegram / Discord)

---

## ⚙️ Core Capabilities

### 1. 📰 News Aggregation
- Fetches the latest crypto news from external APIs (e.g., NewsAPI)
- Filters content based on recency and relevance
- Supports multi-source integration (upgrade-ready)

---

### 2. 🤖 AI Analysis
Leverages AI models to perform:

- Automatic news summarization
- Sentiment analysis:
  - Bullish 📈
  - Bearish 📉
  - Neutral ⚖️
- Entity extraction:
  - Top mentioned coins
  - Key narratives
- Insight generation

---

### 3. 📊 Market Insight Generation
Generates structured outputs such as:

- Daily crypto reports
- Market sentiment overview
- Narrative detection (upgrade-ready)
- Actionable insights for users

---

### 4. 🧾 Structured Output

#### Human-Readable Format:
🔥 CRYPTO DAILY

📊 Sentiment: Bullish

📰 Summary:
...

💰 Top Coins:
BTC, ETH

🧠 Insight:
...

#### JSON Format (AI Layer):
```json
{
  "summary": "...",
  "sentiment": "bullish",
  "topCoins": ["BTC", "ETH"],
  "insight": "..."
}

5. ⏰ Automation
Runs automatically using cron scheduling
Default execution: once per day
Fully configurable via agent settings
6. 🔌 Extensibility

Built with a modular architecture:

tools/ → data collection
core/ → logic & AI processing
outputs/ → distribution layer

Easily extendable to:

Twitter (X) bots
Telegram bots
Discord bots
Trading signal systems
🧠 Agent Behavior Modes
Aggressive Mode
Focuses on trending and high-impact news
Suitable for viral content generation
Conservative Mode
Focuses on reliable and significant updates
Suitable for long-term investors