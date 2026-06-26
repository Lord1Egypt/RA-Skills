# 币安资金费率套利监控 (SkillPay版)

通过 SkillPay 按次付费使用币安账户监控服务。

## 价格

- 每次调用: **1 USDT**
- 支付方式: Crypto 钱包 (Web3)

## 前置要求

使用本工具前，需要配置以下环境变量：

### 必需（用户自己的币安 API）
```bash
export BINANCE_API_KEY="your_binance_api_key"
export BINANCE_API_SECRET="your_binance_api_secret"
```

### 可选（SkillPay 配置，通常由平台自动注入）
```bash
export SKILLPAY_API_KEY="your_skillpay_api_key"
export SKILLPAY_ENDPOINT="https://api.skillpay.me/v1"
```

## 功能

1. **账户总览** - 总权益、已用保证金、可用余额
2. **持仓监控** - 当前持仓、方向、浮动盈亏
3. **资金费统计** - 近7天资金费收入
4. **完整报告** - 一键获取所有信息

## 使用方法

1. 配置币安 API Key
2. 安装 Skill: `clawhub install binance-funding-monitor`
3. 调用功能，按提示支付 1 USDT
4. 获取监控数据

## 免责声明

本工具仅供监控使用，不构成投资建议。交易有风险，投资需谨慎。