# 🦊 媳妇智投全球通用版 | Ai-Wife Global Investing

---

## 📖 Introduction / 简介

**Ai-Wife Global Investing** generates cross-market trading plan **templates** for **52 countries/regions**. User provides a stock symbol — generates an analysis reference framework.

**媳妇智投全球通用版** 生成跨市场交易方案**模板**。覆盖**52个国家/地区**交易所，用户指定股票代码后，生成分析参考框架。

> ⚠️ **Educational Tool Only / 仅限教育用途** — All outputs are for learning and reference. Not investment advice.

---

## ✨ Key Features / 核心特色

| Feature | Description |
|:--------|:------------|
| 🌍 **52 Markets** | A股、美股、港股 + 🇬🇧🇯🇵🇩🇪🇫🇷...52国 |
| 🔍 **Manual Select** | User specifies market + code |
| 📈 **5 Plan Types** | Stock / Futures / Fund / Forex / Crypto |
| 📄 **Word Output** | Professional .docx format |
| 📱 **Bilingual** | Chinese + English |

---

## 🚀 Quick Start / 快速开始

### Install / 安装

```bash
openclaw skill install ai-xifu-caopan
```

### Usage / 使用示例

| You Say / 你说 | I Do / 我做 |
|:---------------|:------------|
| `"分析AAPL"` / `"Analyze NVDA"` | 🇺🇸 Generate analysis template / 生成分析模板 |
| `"看600519"` | 🇨🇳 Generate A-share analysis / 生成A股分析 |
| `"看SHEL.L"` / `"Analyze 7203.T"` | 🇬🇧🇯🇵 Generate market analysis / 生成市场分析 |
| `"帮我出BTC/USD方案"` | ₿ Generate crypto reference / 生成加密分析参考 |

### Symbol Reference / 代码格式参考

| Format / 格式 | Example / 示例 | → |
|:-------------|:---------------|:-:|
| 6位数字 | `600519` `000001` `300750` | 🇨🇳 A-Share |
| 4位数字 | `0700` `00700` | 🇭🇰 HK Stock |
| 纯字母 | `AAPL` `NVDA` `TSLA` | 🇺🇸 US Stock |
| `.L` 后缀 | `SHEL.L` `HSBA.L` `BP.L` | 🇬🇧 UK |
| `.T` 后缀 | `7203.T` `6758.T` | 🇯🇵 Japan |
| `.DE` 后缀 | `SAP.DE` `BAYN.DE` | 🇩🇪 Germany |
| `.KS` 后缀 | `005930.KS` `000660.KS` | 🇰🇷 S.Korea |
| ...and 40+ more | see market_engine.py | 🌍 Global |

---

## 📑 Plan Types / 方案类型

| Plan / 方案 | Chapters | Template |
|:-----------|:--------:|:---------|
| 📊 **Stock / 股票** | 27 chapters | `FINAL_PLAN_TEMPLATE.md` |
| 📦 **Futures / 期货** | 22 chapters | `template_futures_v7.py` |
| 🏦 **Fund / 基金** | 11 chapters | `template_fund_v7.py` |
| 💱 **Forex / 外汇** | 12 chapters | `template_fx_v7.py` |
| ₿ **Crypto / 加密货币** | 10 chapters | `template_crypto_v7.py` |

All are **template frameworks** — users review and customize before use.
均为**模板框架**——用户自行审阅和调整后使用。

---

## ⚙️ Before Using / 使用前准备

> ⚠️ **No built-in API keys!** / 无内置密钥，用户自配。

| Data Source | Markets | Setup |
|:------------|:--------|:------|
| **yfinance** 🌐 | All 52 | `pip3 install yfinance` |
| **Guosen API** | 🇨🇳🇺🇸🇭🇰 | Set `GS_API_KEY` |
| **Sina Finance** | 🇨🇳🇺🇸 | Zero config |

📖 Full guide: `global_market/CONFIG_GUIDE.md`

---

## 📁 File Structure / 文件结构

```
ai-xifu-caopan/
├── SKILL.md                    # Full skill doc
├── README.md                   # Quick start
├── global_market/              # 🌍 Engine
│   ├── market_config.json      # 52-country config
│   ├── market_engine.py        # Market detection
│   └── CONFIG_GUIDE.md         # Config guide
├── templates/                  # 📑 Templates
└── scripts/
```

---

## 📜 Disclaimer / 法律声明

> ⚠️ **Educational Tool Only / 仅限教育用途**
>
> 1. This tool provides **template frameworks** for analysis. It does NOT provide investment advice or trading recommendations.
> 2. This tool has NOT obtained securities/futures investment advisory business qualification.
> 3. All outputs are for **learning and reference only**. Users bear full responsibility for their own decisions.
> 4. Example data in templates is for illustration. Real-time data requires user-configured API access.
>
> **Investing involves risk. Invest at your own risk.**
> **投资有风险，入市需谨慎。**

---

**媳妇智投全球通用版 | Ai-Wife出品 🦊**
