---
name: eth-price-predictor
description: ETH价格预测 - 日/周涨跌方向预测，技术指标+链上数据。每次调用0.003 USDT。
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - SKILLPAY_API_KEY
---

# ETH 价格预测器

**以太坊专属预测工具** - 日/周级别涨跌预测

## 特点

- 技术指标分析（RSI、MACD、布林带）
- 链上数据参考（Gas费、DeFi锁仓）
- 多时间周期（日线、周线）
- ETF资金流向

## 收费模式

每次调用 **0.003 USDT**（约0.021元人民币）

## 使用方法

```bash
# 日线预测（默认）
node scripts/predict.js

# 周线预测
node scripts/predict.js weekly

# 查看ETF资金流向
node scripts/predict.js etf
```

## 输出示例

```
════════════════════════════════════════════════════
📊 ETH 日线预测
════════════════════════════════════════════════════

当前价格: $3,842.15
预测周期: 24小时

🎯 预测: 涨 📈
置信度: 72%

技术指标:
  ✅ RSI(58.2) 偏多 → 看涨
  ✅ MACD 金叉形成 → 看涨
  ➖ BOLL 中轨附近 → 震荡
  ✅ Volume +18% 放量上涨

链上数据:
  Gas费: 32 Gwei (中等)
  DeFi锁仓: +2.3% (资金流入)
  ETF净流入: +$45M

建议: BUY YES
止损: $3,750
止盈: $3,950

════════════════════════════════════════════════════
```

## SkillPay 配置

环境变量：
- `SKILLPAY_API_KEY` - SkillPay API密钥
