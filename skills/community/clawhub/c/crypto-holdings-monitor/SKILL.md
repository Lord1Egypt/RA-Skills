---
name: crypto-holdings-monitor
version: 1.0.0
description: 加密货币持仓监控工具。支持多钱包地址监控、实时价格查询、持仓统计。
author: 你的名字
triggers:
  - "加密货币"
  - "虚拟币持仓"
  - "Crypto"
  - "炒币"
  - "U本位"
---

# Crypto Portfolio Tracker 💰

追踪你的加密货币持仓，支持多钱包地址和实时价格查询。

## 功能

- 📊 支持多钱包地址监控（ETH, BTC, SOL 等）
- 💵 实时 USDC/USD 价格查询
- 📈 持仓统计和占比分析
- 💰 收益计算（按买入价）
- 🔔 定时播报持仓变化

## 使用方法

### 添加钱包地址

```bash
python3 scripts/portfolio.py add 0x...
```

### 查看持仓

```bash
python3 scripts/portfolio.py view
```

### 刷新价格

```bash
python3 scripts/portfolio.py refresh
```

### 完整报告

```bash
python3 scripts/portfolio.py report
```

## 配置

环境变量（可选）：

```bash
# 添加成本价（可选，用于计算收益）
export BTC_COST=45000
export ETH_COST=3000
export SOL_COST=100
```

## 示例

```bash
# 添加钱包
python3 scripts/portfolio.py add 0x742d35Cc6634C0532925a3b844Bc9e7595f0eB1E

# 查看持仓
python3 scripts/portfolio.py view
```
