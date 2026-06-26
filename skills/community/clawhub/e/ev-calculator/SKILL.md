---
name: ev-calculator
description: 🎯 EV 期望值计算器 - 交易决策必备工具
author: Rich
version: 1.0.0
tags:
  - ev
  - expected-value
  - trading
  - probability
  - arbitrage
  - 期望值
openclaw_version: ">=2025.1.0"
# x402收费配置
endpoint: "https://kelly-formula-crypto.vercel.app/api/ev"
auth_type: "x402"
price: "0.01"
currency: "USDC"
chain: "Base"
wallet: "0x24b288c98421d7b447c2d6a6442538d01c5fce22"
capabilities:
  - api_call
---

# 🎯 EV 期望值计算器

**定价**: 0.01 USDC (x402支付)
**作者**: Rich (@samhuang2025)

---

## 简介

计算交易/投注的期望值(Expected Value)，判断是否具有正期望。

**核心功能**：
- ✅ 基础EV计算
- ✅ Polymarket概率计算
- ✅ 赔率转换
- ✅ 套利边界检测

---

## 核心公式

### 基础版
```
EV = p × win - (1-p) × loss
```
- p = 胜率
- win = 赢的金额
- loss = 输的金额

### 简化版（对称盈亏）
```
EV = p × b - (1-p) × 1
```
其中 b = 盈亏比

### Polymarket版
```
EV = 你的概率 - 市场概率
```

---

## 判断标准

| EV值 | 含义 | 行动 |
|------|------|------|
| EV > 0 | 正期望值，能赚 | ✅ 可以玩 |
| EV = 0 | 不亏不赚 | ⚪ 观望 |
| EV < 0 | 负期望值，必亏 | ❌ 不玩 |

---

## 使用方法

### 1. 基础EV计算

```python
def calculate_ev(p, win, loss):
    """
    计算期望值
    
    Args:
        p: 胜率 (0-1)
        win: 赢的金额
        loss: 输的金额
    
    Returns:
        EV值 (正=赚，负=亏)
    """
    return p * win - (1 - p) * loss
```

### 2. Polymarket概率

```python
def polymarket_ev(your_prob, market_price):
    """
    计算Polymarket的EV
    
    Args:
        your_prob: 你判断的真实概率 (0-1)
        market_price: 市场定价 (0-1)
    
    Returns:
        edge (你的概率 - 市场概率)
    """
    return your_prob - market_price
```

### 3. 盈亏比计算

```python
def win_loss_ratio(win_pct, loss_pct):
    """计算盈亏比"""
    return win_pct / loss_pct
```

---

## 实战案例

### 案例1：抛硬币
- 正面赢 $1.10
- 反面输 $1.00
- 概率各 50%

```
EV = 0.5 × 1.10 - 0.5 × 1.00 = +$0.05
```
✅ 每赌一次期望赚5分

### 案例2：Polymarket
- 你判断 Trump 赢 = 60%
- 市场定价 YES = 40%
- 买入成本 = $0.40

```
EV = 0.60 - 0.40 = +0.20 (20% edge)
```
✅ 每投$1期望赚$0.20

### 案例3：彩票套利（Winfall Roll-down）
- 正常时期：期望拿回$0.55
- Roll-down时期：期望拿回$1.18

```
正常EV = 0.55 - 1.00 = -$0.45 (亏)
套利EV = 1.18 - 1.00 = +$0.18 (赚)
```

---

## 快速查询表

### 对称盈亏（赢亏相等）

| 胜率 | EV | 评价 |
|------|-----|------|
| 45% | -10% | 远离 |
| 48% | -4% | 避开 |
| 50% | 0% | 公平 |
| 52% | +4% | 可以 |
| 55% | +10% | 不错 |
| 60% | +20% | 很好 |
| 70% | +40% | 极佳 |

### Polymarket Edge

| 市场定价 | 你的判断 | Edge |
|----------|---------|------|
| 30% | 45% | +15% |
| 40% | 55% | +15% |
| 50% | 65% | +15% |
| 60% | 75% | +15% |

---

## 代码实现

```python
#!/usr/bin/env python3
"""EV Calculator"""

import argparse
import json

def calculate_ev(p, win, loss):
    return p * win - (1 - p) * loss

def polymarket_ev(your_prob, market_price):
    edge = your_prob - market_price
    ev_dollar = edge / market_price if market_price > 0 else 0
    return edge, ev_dollar

def main():
    parser = argparse.ArgumentParser(description="EV Calculator")
    parser.add_argument("--p", type=float, help="胜率 (0-1)")
    parser.add_argument("--win", type=float, help="赢的金额")
    parser.add_argument("--loss", type=float, help="输的金额")
    parser.add_argument("--market", type=float, help="市场定价 (Polymarket)")
    parser.add_argument("--your", type=float, help="你的判断概率")
    parser.add_argument("--json", action="store_true")
    
    args = parser.parse_args()
    
    if args.p and args.win and args.loss:
        ev = calculate_ev(args.p, args.win, args.loss)
        result = {
            "type": "basic",
            "ev": ev,
            "verdict": "✅ 正期望" if ev > 0 else "❌ 负期望" if ev < 0 else "⚪ 持平"
        }
    elif args.market and args.your:
        edge, ev = polymarket_ev(args.your, args.market)
        result = {
            "type": "polymarket",
            "market_price": args.market,
            "your_prob": args.your,
            "edge": edge,
            "ev_per_dollar": ev,
            "verdict": "✅ 正期望" if edge > 0 else "❌ 负期望"
        }
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"\n🎯 EV计算结果")
        print(f"=" * 30)
        if result["type"] == "basic":
            print(f"胜率: {args.p*100:.0f}% | 赢: ${args.win} | 亏: ${args.loss}")
            print(f"EV: ${result['ev']:.2f}")
        else:
            print(f"市场定价: {args.market*100:.0f}% | 你的判断: {args.your*100:.0f}%")
            print(f"Edge: {result['edge']*100:.0f}%")
            print(f"每$期望赚: ${result['ev_per_dollar']:.2f}")
        print(f"\n{result['verdict']}")

if __name__ == "__main__":
    main()
```

---

## 风险提示

- EV是基于历史数据的期望，不代表未来
- 实际执行需考虑滑点、费率、资金费等摩擦成本
- 慎用小样本数据，容易产生偏差

---

## 相关资源

- 配套Skill: kelly-formula-crypto (凯利公式仓位管理)
- MEMORY.md: Polymarket交易系统完整指南

---

## 更新日志

- 2026-03-20: 初始版本
