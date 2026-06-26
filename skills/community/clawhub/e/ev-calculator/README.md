# EV Calculator - 期望值计算器

<div align="center">

**交易决策必备的EV计算工具**

定价: **0.01 USDC** (x402支付)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

</div>

---

## 🎯 简介

计算交易/投注的期望值(Expected Value)，判断是否具有正期望。

**核心功能**：
- ✅ 基础EV计算
- ✅ Polymarket概率计算
- ✅ 盈亏比转换
- ✅ 凯利仓位建议
- ✅ x402微支付支持

---

## 💰 价格

**0.01 USDC** - 通过x402协议支付

```bash
# 支付示例
curl -X POST https://api.x402.dev/pay \
  -H "Content-Type: application/json" \
  -d '{
    "to": "0x24b288c98421d7b447c2d6a6442538d01c5fce22",
    "amount": "0.01",
    "currency": "USDC",
    "memo": "ev-calculator"
  }'
```

---

## 📖 核心公式

### 基础版
```
EV = p × win - (1-p) × loss
```

### Polymarket版
```
EV = 你的概率 - 市场概率
```

---

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/jinboh68-prog/ev-calculator.git
cd ev-calculator
pip install -r requirements.txt
```

### 使用

```bash
# 基础EV计算
python scripts/ev_calculator.py --p 0.55 --win 1.10 --loss 1.00

# Polymarket EV
python scripts/ev_calculator.py --market 0.40 --your 0.60

# 带盈亏比
python scripts/ev_calculator.py --p 0.60 --win 5 --loss 3 --b 1.67

# JSON输出
python scripts/ev_calculator.py --p 0.55 --win 1.10 --loss 1.00 --json
```

---

## 📊 实战案例

### 案例1：抛硬币
```
胜率: 50%, 赢: $1.10, 亏: $1.00
EV = 0.5 × 1.10 - 0.5 × 1.00 = +$0.05
✅ 每赌一次期望赚5分
```

### 案例2：Polymarket
```
市场定价: 40%, 你的判断: 60%
Edge = 60% - 40% = +20%
每投$1期望赚$0.20
```

---

## 📋 判断标准

| EV值 | 含义 | 行动 |
|------|------|------|
| EV > 0 | 正期望值 | ✅ 可以玩 |
| EV = 0 | 不亏不赚 | ⚪ 观望 |
| EV < 0 | 负期望值 | ❌ 不玩 |

---

## ⚠️ 风险提示

- EV是基于历史数据的期望，不代表未来
- 实际执行需考虑滑点、费率、资金费等摩擦成本
- 慎用小样本数据，容易产生偏差

---

## 📝 License

MIT License

---

## 🔗 相关链接

- GitHub: https://github.com/jinboh68-prog/ev-calculator
- 配套: kelly-formula-crypto (凯利公式仓位管理)
- 作者: @samhuang2025
