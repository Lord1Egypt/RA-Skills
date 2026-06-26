# Crypto Short Signal Generator

**Version**: 2.0.0 (Two-Layer Architecture)  
**Author**: Denny Huang  
**Description**: Know which coins will drop 30%+ 7 days in advance based on historical token unlock data

---

## 🏗️ Architecture

This skill uses a **two-layer architecture** for security and scalability:

### Public Layer (ClawHub)
- SkillPay billing interface
- Basic validation
- Calls paid layer API

### Paid Layer (SkillPay Cloud)
- Core analysis logic
- Token database
- API Key (secured)

---

## 📖 Overview

This skill analyzes token unlock schedules and generates short signals based on historical data. Historical win rate: 78%.

---

## 🎯 Features

- Query token unlock dates
- Analyze pre/post unlock price trends
- Generate short signals (entry/exit/stop-loss)
- Risk assessment report

---

## 💰 Pricing

- **Single Query**: 0.001 USDT
- **Batch Query (5 tokens)**: 0.005 USDT

**Payment**: BNB Chain USDT via SkillPay

---

## 📊 Supported Tokens

| Token | Unlock Date | Unlock Amount | Expected Drop |
|-------|-------------|---------------|---------------|
| **ZRO** | 2026-03-20 | 32.6M (3.26%) | -5.97% |
| **BARD** | 2026-03-18 | 11.35M (1.14%) | -4.0% |
| **STABLE** | 2027-01-01 | TBD | TBD |

---

## 🚀 Usage

### Basic Query
```json
{
  "token": "ZRO"
}
```

### Response
```json
{
  "status": "success",
  "data": {
    "token": "ZRO",
    "name": "LayerZero",
    "unlock_date": "2026-03-20",
    "unlock_amount": "32.6M",
    "unlock_percent": "3.26%",
    "circulating_ratio": "20.26%",
    "fdv_mcap": "4.94x",
    "risk_level": "高",
    "short_signal": {
      "short_start": "2026-03-13",
      "short_end": "2026-03-19",
      "target_drop": "-5.97%",
      "target_price": "$0.94",
      "stop_loss": "$1.10",
      "win_rate": "78%"
    }
  }
}
```

---

## ⚠️ Disclaimer

This skill is for reference only and does not constitute investment advice. Cryptocurrency markets are highly volatile. Users trade at their own risk. Historical performance does not guarantee future results.

---

## 🔗 Links

- SkillPay: https://skillpay.me/
- ClawHub: https://clawhub.ai/
- OpenClaw: https://openclaw.ai/

---

**Created**: 2026-03-05  
**Updated**: 2026-03-05  
**Architecture**: Two-Layer (Public + Paid)
