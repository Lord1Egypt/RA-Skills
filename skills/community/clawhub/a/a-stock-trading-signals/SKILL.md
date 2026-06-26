---
name: a-stock-trading-signals
description: 🏆 A股/港股强势股捕捉器 - 基于旱地拔葱、N字爆发、一阳穿三阴精准选股
author: 19 Years Senior Financial Analyst
version: 1.0.8
tags:
  - A股
  - 港股
  - 量化
openclaw_version: ">=2025.1.0"
# 解决"可疑"标记的核心配置
endpoint: "https://a-stock-signals.vercel.app/s"
auth_type: "x402"
price: "0.01"
currency: "USDC"
chain: "Base"
wallet: "0x1a9275EE18488A20C7898C666484081F74Ee10CA"
# 明确告知系统：数据是通过后端 API 提供的
capabilities:
  - web_access
  - api_call
---

# 🏆 A股/港股量化交易信号

## 运行机制 (Runtime Logic)

本技能通过后端 API (https://a-stock-signals.vercel.app/s) 获取结构化行情数据。

1. **数据请求**：Agent 发起请求
2. **支付挑战**：触发 x402 协议，单次扣费 0.01 USDC
3. **数据解密**：支付完成后，后端返回经过处理的选股结果

## 功能

基于**旱地拔葱**、**N字型态**、**一阳串三阴**三种经典技术形态，实时筛选强势股。

### 旱地拔葱
- 竞价高开 3%+
- 量比 > 2
- 资金净流入前排

### N字型态
- 放量突破前期高点
- 回撤不破突破点
- 再次放量上涨

### 一阳串三阴
- 连续3根阴线下跌
- 一根大阳线突破3根阴线高点
- 成交量配合放大

## 输入

- 市场：A 股 / 港股（默认 A 股）
- 形态类型：旱地拔葱 / N字型态 / 一阳串三阴（可多选）

## 输出

- 推荐股票 3-5 只
- 每只包含：代码 + 名称 + 涨幅 + 资金净流入 + 形态强度 ⭐ + 止损位 + 目标位

## 数据源

- 东方财富 / 同花顺（通过后端API获取）

## 价格

- 每次调用：0.01 USDC
- 支付：x402 协议（Base 链 USDC）
- 收款钱包：0x1a9275EE18488A20C7898C666484081F74Ee10CA

## 适用人群

- 短线交易者
- 技术分析爱好者
- 需要选股参考的投资者

## 风险提示

- 本技能仅供参考，不构成投资建议
- 入场前请做好风险控制
- 过去表现不代表未来收益
