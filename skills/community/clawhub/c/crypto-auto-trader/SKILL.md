---
name: crypto-auto-trader
description: >
  多平台通用AI自动交易策略包。5大策略完整源码+部署教程，
  适用于OKX/币安/Bybit/Bitget。含风控+报警模块。
version: 1.0.0
tags: [trading, crypto, bot, strategy, auto-trader, ccxt]
license: MIT
author: Vane
repository: https://github.com/sgready/vane-signals
---

# Crypto Auto-Trader Strategy Bundle

多平台通用AI自动交易策略包，包含完整Node.js源码和部署教程。适用于OKX/币安/Bybit/Bitget等主流交易所。

## 产品内容

### 本包包含
1. **《AI自动交易策略实战手册》**（PDF格式）
2. **5套策略完整源码**
3. **风控模块（可配置参数）**
4. **Telegram报警集成**
5. **OKX/币安双模板**

### 策略清单
| 策略 | 逻辑 | 适用场景 |
|------|------|---------|
| EMA金叉死叉 | 3日/26日EMA交叉 | 趋势行情 |
| BOLL上轨做空 | 布林带上轨+WR超买 | 震荡/回调 |
| Serenity低吸 | RSI<20深度回调 | 暴跌抄底 |
| 多周期共振 | 15min/1h/4h三重确认 | 趋势确认 |
| FusionEngine | 6交易员加权投票 | 全市场通用 |

### 部署环境
- Node.js 18+
- CCXT 4.x
- Windows/Mac/Linux 全平台
- PM2 进程守护

## 安装
```bash
npm install ccxt https-proxy-agent
```

## 快速开始
1. 解压源码包
2. 编辑 `config.json` 填入你的API Key
3. `npm install`
4. `pm2 start auto_trader.js`

## 版本历史
- v1.0: 首发版，5策略+风控+报警

---

*注意：本产品为知识付费，不构成投资建议。加密合约交易风险极高，请合理控制仓位。*
