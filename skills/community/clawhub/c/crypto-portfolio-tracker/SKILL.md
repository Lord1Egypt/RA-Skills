---
name: crypto-portfolio-tracker
description: 加密貨幣Portfolio追蹤 - 支援TRON/ETH/BSC，分析持倉、收益、Gas費用
version: 1.0.0
tags:
  - crypto
  - defi
  - tron
  - eth
  - portfolio
  - tracking
---

# Crypto Portfolio Tracker

追蹤你既加密貨幣投資組合。

## 支援網絡

- 🌐 TRON (TRC20)
- 🔷 Ethereum (ERC20)
- 🔶 BSC (BEP20)

## 功能

- 💰 餘額查詢
- 📊 持倉分析
- 📈 收益計算
- ⛽ Gas費用追蹤
- 🔔 價格alert (optional)

## 使用

```bash
# TRON餘額
tron wallet --address TXXX... balance

# 查詢代幣
tron token --address TXXX... balance --symbol USDT
```

## 整合

可以配合 Sunswap DEX skill 做swap分析。
