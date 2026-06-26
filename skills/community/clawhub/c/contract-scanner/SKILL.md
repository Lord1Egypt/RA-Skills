---
name: contract-scanner
version: 1.0.0
description: |
  Scan smart contracts for security risks.
  Detect honeypots, high taxes, and malicious code.
  Protect yourself from scams!
metadata:
  openclaw:
    emoji: 🛡️
    requires:
      env:
        - ETHERSCAN_API_KEY
      bins:
        - python3
        - curl
  pricing:
    type: freemium
    free:
      description: "每日 3 次检测"
      limits:
        dailyScans: 3
    pro:
      price: 1.99
      currency: USD
      period: monthly
      description: "无限检测，实时风险告警"
      features:
        - "无限合约检测"
        - "实时风险告警"
        - "代码深度分析"
        - "历史安全评分"
        - "批量检测"
        - "API 访问"
---

# 🛡️ Contract Scanner - 合约安全检测

Scan smart contracts for security risks and scams.

## Features

- 🔍 Honeypot detection
- 💸 Tax analysis (buy/sell)
- 🔐 Ownership check
- 📊 Risk scoring
- ⚠️ Real-time alerts

## Usage

```bash
# Scan a contract
/contract-scanner check 0x123...abc

# Check tax
/contract-scanner tax 0x123...abc

# Verify ownership
/contract-scanner owner 0x123...abc
```

## Risk Levels

- 🟢 **Low** - Safe to trade
- 🟡 **Medium** - Some risks, be careful
- 🟠 **High** - High risk, avoid
- 🔴 **Critical** - Scam/honeypot, DO NOT BUY

