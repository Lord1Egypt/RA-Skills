---
name: btc-strategy-v40
description: |
  BTC V4.0 量化交易策略 - 基于 EMA3/EMA8 交叉、RSI 和动量的多因子信号系统。
  提供实时价格监控、技术信号生成、自动通知功能。
  适用于 BTC 永续合约的 10x 杠杆交易策略。
metadata:
  author: qianzhentao1
  version: "4.0.0"
  tags: [trading, btc, crypto, strategy, signals]
---

# BTC V4.0 交易策略

## 概述

基于多因子加权评分的 BTC 量化交易策略：
- **EMA3/EMA8 交叉** (权重 2x)
- **RSI 超买超卖** (权重 1x)
- **价格动量** (权重 1.5x)
- **支撑/阻力位** (权重 1x)

## 信号阈值

| 信号 | 阈值 | 条件 |
|------|------|------|
| 做多 | ≥1 | 加权评分 ≥ 1 |
| 做空 | ≤-1 | 加权评分 ≤ -1 |
| 观望 | -1~1 | 无明确信号 |

## 使用方法

### 启动监控

```bash
bash scripts/btc_signal_monitor_v40_fixed.sh
```

### 运行策略分析

```bash
python3 scripts/btc_10x_strategy_v40.py
```

### 查看当前信号

```bash
# 获取当前 BTC 价格和信号
curl -s "https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT-SWAP" | jq '.data[0]'
```

## 监控配置

- **检查频率**: 每1分钟
- **价格源**: OKX API + 备用源
- **通知方式**: Telegram Bot
- **日志位置**: `/tmp/btc_v40_monitor.log`

## 策略参数

| 参数 | 值 | 说明 |
|------|-----|------|
| EMA 短周期 | 3 | 快速 EMA |
| EMA 长周期 | 8 | 慢速 EMA |
| RSI 做多阈值 | 35 | 超卖区间 |
| RSI 做空阈值 | 65 | 超买区间 |
| 动量做多阈值 | 1.5% | 上涨动能 |
| 动量做空阈值 | -1.5% | 下跌动能 |

## 风险管理

- 建议杠杆: 10x
- 止损设置: 根据 ATR 动态计算
- 仓位管理: 信号强度决定仓位大小

## 文件说明

- `scripts/btc_10x_strategy_v40.py` - 核心策略逻辑
- `scripts/btc_signal_monitor_v40_fixed.sh` - 监控脚本

## 依赖

- Python 3.8+
- requests
- python-telegram-bot (可选，用于通知)
