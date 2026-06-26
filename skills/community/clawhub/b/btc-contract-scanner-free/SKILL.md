---
name: btc-contract-scanner-free
description: >
  BTC合约扫描入门版。5策略实时信号(EMA/MACD/RSI/布林/放量)，1H+4H双时间帧，
  带回测数据。免费使用。Pro版有walkforward自优化+多币种。
version: 1.0.0
tags: [btc, trading, scanner, free, crypto, contract]
license: MIT
author: Vane
repository: https://github.com/sgready/vane-signals
---

# BTC Contract Scanner (Free)

## 简介
BTC合约趋势扫描器，集成5个经典技术指标，输出LONG/SHORT/HOLD信号。
每天UTC 00:00自动运行一次回测验证，附7日回测记录。

## 功能
- ✅ EMA50趋势判断（1H + 4H双时间帧）
- ✅ MACD多空信号
- ✅ RSI超买超卖检测
- ✅ 布林带突破检测
- ✅ 成交量放量确认
- ✅ 每日回测记录（7天滚动）
- ✅ 信号输出JSON格式

## 回测数据样例（最近7天）
```
date       | direction | entry   | exit    | pnl%  | status
2026-06-07 | HOLD      | 62800   | 63091   | +0.46 | ✓
2026-06-06 | SHORT     | 63500   | 62800   | +1.10 | ✓
2026-06-05 | LONG      | 64200   | 63500   | -1.09 | ✗
2026-06-04 | HOLD      | 63800   | 64200   | +0.63 | ✓
2026-06-03 | HOLD      | 64100   | 63800   | -0.47 | ✗
2026-06-02 | LONG      | 62500   | 64100   | +2.56 | ✓
2026-06-01 | HOLD      | 61900   | 62500   | +0.97 | ✓
```

**7日胜率: 71.4% | 总PnL: +4.16%**

## 使用方法
```bash
# 安装
clawhub install btc-contract-scanner-free

# 运行
openclaw run btc-contract-scanner-free

# 输出JSON
{
  "price": 63091,
  "regime": "ranging",
  "long_score": 2.1,
  "short_score": 1.5,
  "decision": "hold",
  "last_backtest": "2026-06-07",
  "backtest_7d_winrate": 71.4,
  "backtest_7d_pnl": 4.16
}
```

## 数据来源
- OKX实时行情（通过Clash代理）
- 无需API Key

## 限制
- ❌ 仅BTC/USDT
- ❌ 无walkforward自优化
- ❌ 无资金管理建议
- ❌ 无多币种支持

## 升级
需要完整版？安装 Pro 版获得：
- ✅ walkforward网格自优化
- ✅ SOL/ETH多币种
- ✅ 资金管理模块
- ✅ Telegram推送
- ✅ 实时警报

## 安装
`clawhub install btc-contract-scanner-pro`
