---
name: a-stock-vcp
description: 📈 A股强势股捕捉器 - 基于VCP放量突破形态，精准捕捉强势启动点
author: 19 Years Senior Financial Analyst
version: 1.0.8
tags:
  - A股
  - VCP
  - 量化
openclaw_version: ">=2025.1.0"
# 解决"可疑"标记的核心配置
endpoint: "https://a-stock-signals.vercel.app/v"
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

# 📈 A股强势股捕捉器 (VCP)

## 运行机制 (Runtime Logic)

本技能通过后端 API (https://a-stock-signals.vercel.app/v) 获取结构化行情数据。

1. **数据请求**：Agent 发起请求
2. **支付挑战**：触发 x402 协议，单次扣费 0.01 USDC
3. **数据解密**：支付完成后，后端返回经过处理的 VCP 放量突破筛选结果

## 功能

基于 **VCP (Volatility Contraction Pattern)** 放量突破形态，精准捕捉强势启动点。

### VCP特征

- 股价在一定区间内波动收缩
- 成交量逐渐萎缩
- 放量突破区间上沿
- 突破时成交量明显放大

## 输入

- 市场：A股（默认）
- 形态类型：VCP放量突破

## 输出

- 推荐股票 3-5 只
- 每只包含：
  - 代码 + 名称
  - 所处板块
  - 当前价格
  - 涨幅
  - 放量情况
  - 强势度 ⭐⭐⭐/⭐⭐/⭐
  - 止损位 + 目标位
  - 买入理由

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
- 入场前请做好风险控制（建议-5%止损）
- 过去表现不代表未来收益
