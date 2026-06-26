---
name: airdrop-alert
version: 1.0.0
description: |
  Monitor and track potential crypto airdrops.
  Get alerts for new airdrop opportunities.
  Never miss an airdrop again!
metadata:
  openclaw:
    emoji: 🪂
    requires:
      env:
        - TELEGRAM_BOT_TOKEN
      bins:
        - python3
        - curl
  pricing:
    type: freemium
    free:
      description: "每日 5 个空投提醒"
      limits:
        dailyAlerts: 5
    pro:
      price: 1.99
      currency: USD
      period: monthly
      description: "无限空投提醒，早期项目优先"
      features:
        - "无限空投提醒"
        - "早期项目优先通知"
        - "空投资格检测"
        - "任务清单自动生成"
        - "多账户管理"
        - "预期价值评估"
---

# 🪂 Airdrop Hunter - 空投监控器

Track and monitor crypto airdrop opportunities.

## Features

- 🔍 Discover new airdrops early
- 📋 Auto-generate task lists
- 💰 Estimate airdrop value
- 📱 Telegram alerts
- 🎯 Eligibility checker

## Usage

```bash
# Check new airdrops
/airdrop-hunter new

# Check eligibility
/airdrop-hunter check <wallet_address>

# Set alerts
/airdrop-hunter alert --min-value 100
```

