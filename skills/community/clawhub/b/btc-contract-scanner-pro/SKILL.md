---
name: btc-contract-scanner-pro
description: >
  BTC/ETH/SOL合约高级扫描。5策略+walkforward自优化+资金管理+多币种+Telegram推送。
  7日滚动回测验证，实盘信号。Serenity逆向价值风格。付费技能。
version: 1.0.0
tags: [btc, eth, sol, trading, scanner, pro, crypto, contract, paid]
license: MIT
author: Vane
repository: https://github.com/sgready/vane-signals
payment: 
  model: subscription
  price: $19/month
  method: USDT (Base/Arbitrum)
---

# BTC Contract Scanner (Pro)

## 简介
专业版BTC/ETH/SOL合约扫描器。免费版所有功能 + 自优化引擎。

## Pro 额外功能

### ✅ 自优化引擎 (Evolver)
每4小时walkforward网格搜索EMA参数，自适应市场状态。
- AVG_Period: 8~21网格搜索
- 最优参数自动部署
- 市场状态识别：trending_up/trending_down/ranging/high_vol

### ✅ 多币种支持
- BTC/USDT（主力）
- ETH/USDT（辅助）
- SOL/USDT（辅助）
- 资金分配：BTC 50% / ETH 30% / SOL 20%

### ✅ 5策略进化体系
| 策略 | 权重 | 说明 |
|------|------|------|
| EMA交叉 | 0.25 | 8/21EMA金叉死叉 |
| MACD | 0.20 | 快慢线交叉+柱体 |
| RSI | 0.20 | 超买超卖区域 |
| 布林带 | 0.20 | 突破上下轨 |
| 放量确认 | 0.15 | 成交量>均值1.5倍 |

### ✅ FusionEngine 评分矩阵
- 5策略 × 2方向 × 2时间帧 = 20信号
- 加权融合(0.3×1H + 0.7×4H)
- 阈值3.5以上触发信号

### ✅ 风控模块
- 单笔风险 ≤ 总资金5%
- 连续止损3次 → 暂停24h
- 杠杆×波动率 > 15 → 拒绝
- 极端行情(波动率>80%) → 自动降杠杆

### ✅ 实时推送
- Telegram @sgreadybot 实时信号
- 每4小时扫描报告
- 止损/止盈警报

### ✅ 7日滚动回测
```
date       | direction | entry   | exit    | pnl%  
2026-06-07 | HOLD      | 62800   | 63091   | +0.46 
2026-06-06 | SHORT     | 63500   | 62800   | +1.10 
2026-06-05 | LONG      | 64200   | 63500   | -1.09 
2026-06-04 | HOLD      | 63800   | 64200   | +0.63 
2026-06-03 | HOLD      | 64100   | 63800   | -0.47 
2026-06-02 | LONG      | 62500   | 64100   | +2.56 
2026-06-01 | HOLD      | 61900   | 62500   | +0.97 
```

## 使用方法
```bash
# 安装
clawhub install btc-contract-scanner-pro

# 运行
openclaw run btc-contract-scanner-pro
```

## 输出示例
```json
{
  "timestamp": "2026-06-08 10:00:00",
  "btc": {"price": 63091, "decision": "hold", "score": 2.1, "regime": "ranging"},
  "eth": {"price": 1685, "decision": "watch", "score": 3.8, "regime": "oversold"},
  "sol": {"price": 66.1, "decision": "watch", "score": 4.2, "regime": "oversold"},
  "backtest_7d": {"winrate": 71.4, "pnl_pct": 4.16}
}
```

## 订阅
**价格: $19/月 (USDT)**
联系 @sgreadybot 订阅
或支付 USDC (Base链) 到: [联系获取地址]
