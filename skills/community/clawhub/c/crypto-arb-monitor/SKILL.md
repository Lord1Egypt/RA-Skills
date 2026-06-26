---
name: crypto-arb-monitor
version: 1.0.0
description: "加密货币跨交易所套利监控器 - 实时监控BTC/ETH/SOL等主流币种在不同交易所的价差，发现套利机会并发送飞书/Telegram预警。支持自动计算手续费后净利润。"
author: 小琳 (SmartChain Capital)
license: MIT
platforms:
  - openclaw
tags:
  - cryptocurrency
  - arbitrage
  - trading
  - monitoring
  - feishu
  - defi
price: 29
---

# Crypto Arbitrage Monitor 🔍💰

**跨交易所加密货币套利机会监控器**

实时监控主流加密货币在不同交易所之间的价格差异，发现套利机会并推送预警。

## 功能特性

- ✅ 支持 Binance / OKX / Bybit / Huobi 等主流交易所
- ✅ 监控 BTC / ETH / SOL / XRP / DOGE 等热门币种
- ✅ 自动计算扣除手续费后的净利润
- ✅ 飞书/Telegram实时预警推送
- ✅ 可配置价差阈值和监控频率
- ✅ 历史套利机会记录和统计

## 快速开始

### 1. 安装依赖

```bash
pip install ccxt requests python-dotenv
```

### 2. 配置

```python
# config.py
CONFIG = {
    "exchanges": ["binance", "okx", "bybit"],
    "symbols": ["BTC/USDT", "ETH/USDT", "SOL/USDT", "XRP/USDT", "DOGE/USDT"],
    "min_spread_percent": 0.5,  # 最小价差百分比（扣除手续费后）
    "trading_fee_percent": 0.1,  # 单边手续费百分比
    "check_interval_seconds": 60,  # 检查间隔
    "alert_channels": {
        "feishu_webhook": "",  # 飞书机器人webhook地址
        "telegram_bot_token": "",  # Telegram Bot Token
        "telegram_chat_id": "",  # Telegram Chat ID
    }
}
```

### 3. 运行

```bash
python monitor.py
```

## 使用场景

| 场景 | 说明 |
|------|------|
| 手动套利 | 发现价差后手动在两个交易所分别买卖 |
| 网格交易辅助 | 配合网格策略，在价差扩大时增加仓位 |
| 市场监控 | 了解不同交易所的流动性差异 |
| 量化策略输入 | 将价差数据作为量化交易信号 |

## 套利计算公式

```
净利润 = (高价交易所卖出价 - 低价交易所买入价) / 低价交易所买入价 × 100% - 2 × 手续费%
```

只有当净利润 > 阈值时才触发预警。

## 风险提示

- ⚠️ 价差可能在执行过程中消失（执行风险）
- ⚠️ 需要两个交易所都有资金（资金效率）
- ⚠️ 提币/转账需要时间（时间风险）
- ⚠️ 交易所可能有提币限制（流动性风险）
- ⚠️ 本工具仅供监控参考，不构成投资建议

## 文件结构

```
crypto-arb-monitor/
├── SKILL.md          # 技能说明
├── monitor.py        # 主监控脚本
├── config.py         # 配置文件
├── alerts.py         # 预警推送模块
├── requirements.txt  # Python依赖
└── README.md         # 使用说明
```

## 版本历史

- v1.0.0 (2026-03-21): 初始版本，支持多交易所价差监控
