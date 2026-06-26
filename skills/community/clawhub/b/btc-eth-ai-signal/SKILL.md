---
name: crypto-ai-analyst
description: BTC/ETH 交易分析系统。AI技术分析、开仓建议、多平台推送。
version: 1.0.0
metadata:
  openclaw:
    emoji: "🤖"
    tags: ["crypto", "BTC", "ETH", "trading", "analysis"]
---

# 🤖 BTC/ETH AI Trader

AI 驱动的加密货币交易分析系统。自动分析 BTC 和 ETH 行情，基于技术指标生成开仓建议，推送至飞书/Telegram/Discord/企业微信。

数据源：CoinEx（国内直连）。只需配置一个渠道即可使用。

## 功能

- BTC/ETH 实时行情 + AI 技术分析（RSI/MACD/MA/布林带/ATR）
- 开仓建议（入场区间、目标价、止损位、盈亏比）
- 多平台推送（飞书 / Telegram / Discord / 企业微信）
- 每30分钟自动推送

## 安装

编辑 config.json，配置你的推送渠道（飞书/Telegram/Discord/企业微信）。

```bash
python3 scripts/advise.py   # 查看分析报告
python3 scripts/push.py     # 推送到已配置的平台
```

## 风险提示

仅分析参考，不构成投资建议。
