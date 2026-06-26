---
name: binance-funding-monitor
description: 币安资金费率套利监控工具 - 查看账户、持仓、盈亏统计，SkillPay收费版
version: 1.0.3
author: partner
---

# Binance Funding Monitor (SkillPay)

币安资金费率套利监控工具 - 按次付费版

## 价格

- 每次调用: **1 USDT**
- 支付方式: Crypto 钱包 (Web3)

## 前置要求

### 必需环境变量
- `BINANCE_API_KEY` - 币安 API Key
- `BINANCE_API_SECRET` - 币安 API Secret

### 可选环境变量
- `SKILLPAY_API_KEY` - SkillPay API Key（平台自动注入）
- `SKILLPAY_ENDPOINT` - SkillPay API 端点

## 功能

- `get_account_summary` - 账户总览（权益、保证金、余额）
- `get_positions` - 当前持仓列表
- `get_funding_income` - 近7天资金费收入
- `get_full_report` - 完整监控报告

## 配置示例

```bash
export BINANCE_API_KEY="your_api_key"
export BINANCE_API_SECRET="your_api_secret"
```

## 免责声明

本工具仅供监控使用，不构成投资建议。