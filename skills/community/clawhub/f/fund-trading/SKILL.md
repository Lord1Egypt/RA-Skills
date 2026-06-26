---
name: fund-trading
description: 基金实盘交易工具，支持账户管理、基金查询、申购赎回、资产查询
version: 1.0.2
author: weiqitong
license: MIT
tags:
  - fund
  - trading
  - investment
  - finance
  - 基金
  - 交易
metadata:
  openclaw:
    requires:
      bins:
        - python3
    primaryEnv: OPENAPI_URL
---

# Fund Trading - 基金实盘交易

基金实盘交易工具，支持账户管理、基金查询、推荐基金、申购、赎回、撤单、资产查询、交易查询。

## ⚠️ 重要声明

> **真实基金净值，虚拟资金交易**
> 
> - 📊 **基金净值和行情数据** - 来自真实市场，实时更新
> - 💰 **交易资金** - 虚拟模拟资金，仅供学习和测试
> - 🎯 **适用场景** - 投资学习、策略测试、模拟交易

## ✨ 功能特性

- 📝 **账户管理** - 注册、切换、查看账户
- 📊 **基金查询** - 列表、详情、推荐基金
- 💰 **交易操作** - 申购、赎回、撤单
- 📈 **资产查询** - 持仓、收益、交易记录
- 🔐 **OAuth 2.0** - 安全认证，Token 自动刷新

## 📦 安装

### Python (PyPI)

```bash
pip install fund-trading-skill
```

### TypeScript (npm)

```bash
npm install -g fund-trading-skill
```

## 🚀 快速开始

### 注册账户

```bash
fund-trading register --username 我的账户
```

### 查询持仓

```bash
fund-trading position
```

输出示例：

```
┌──────────────────────────────────────────────────┐
│                   💰 资产概览                      │
├──────────────────────────────────────────────────┤
│  总资产: 10000.00元                               │
│  总收益: 📈 +200.00元 (+2.00%)                    │
└──────────────────────────────────────────────────┘
```

### 申购基金

```bash
fund-trading subscribe --fund-code 000001 --amount 1000
```

## 📋 命令参考

| 命令 | 说明 |
|------|------|
| `fund-trading register --username <name>` | 注册新账户 |
| `fund-trading account --list` | 查看账户列表 |
| `fund-trading account --switch <id>` | 切换账户 |
| `fund-trading list` | 查询基金列表 |
| `fund-trading detail --fund-code <code>` | 查询基金详情 |
| `fund-trading recommend` | 获取推荐基金 |
| `fund-trading position` | 查询持仓 |
| `fund-trading orders` | 查询交易记录 |
| `fund-trading subscribe --fund-code <code> --amount <金额>` | 申购基金 |
| `fund-trading redeem --fund-code <code> --shares <份额>` | 赎回基金 |
| `fund-trading cancel --trade-id <订单号>` | 撤销订单 |
| `fund-trading refresh-token` | 刷新 Token |

## 🔧 配置

配置文件位置：`~/.config/opencode/skills/fund-trading/data/config.json`

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `OPENAPI_URL` | API 服务地址 | `https://openapi.nicaifu.com/openApi` |

## 🔐 认证方式

使用 **OAuth 2.0 Client Credentials** 模式：

1. 调用 `/openapi/v1/oauth/token` 获取 JWT Token
2. 使用 `Authorization: Bearer {token}` 调用业务 API
3. Token 自动缓存，过期前 5 分钟自动刷新

## 📡 API 端点

| 功能 | 路径 | 方法 |
|------|------|------|
| Token | `/openapi/v1/oauth/token` | POST |
| 注册 | `/openapi/v1/channel/register` | POST |
| 基金列表 | `/openapi/v1/shipan/fund/list` | GET |
| 基金详情 | `/openapi/v1/shipan/fund/detail` | GET |
| 持仓查询 | `/openapi/v1/shipan/asset/query` | POST |
| 交易查询 | `/openapi/v1/shipan/trade/query` | POST |
| 申购 | `/openapi/v1/shipan/trade/subscribe` | POST |
| 赎回 | `/openapi/v1/shipan/trade/redeem` | POST |
| 撤单 | `/openapi/v1/shipan/trade/cancel` | POST |

## 📚 相关链接

- [PyPI](https://pypi.org/project/fund-trading-skill/)
- [npm](https://www.npmjs.com/package/fund-trading-skill)
- [安装手册](https://github.com/weiqitong/fund-trading-skill/blob/main/INSTALL.md)

## 📄 许可证

MIT License

## 👤 作者

weiqitong (weiqitong@nicaifu.com)