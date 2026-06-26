# Fund Trading Skill

<div align="center">

**基金实盘交易工具**

支持账户管理、基金查询、申购赎回、资产查询

[![PyPI](https://img.shields.io/pypi/v/fund-trading-skill.svg)](https://pypi.org/project/fund-trading-skill/)
[![npm](https://img.shields.io/npm/v/fund-trading-skill.svg)](https://www.npmjs.com/package/fund-trading-skill)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 🎯 简介

Fund Trading Skill 是一个完整的基金实盘交易工具，为 OpenClaw/OpenCode 提供基金交易能力。支持账户管理、基金查询、申购赎回、资产查询等功能。

## ⚠️ 重要声明

> **真实基金净值，虚拟资金交易**
> 
> - 📊 **基金净值和行情数据** - 来自真实市场，实时更新
> - 💰 **交易资金** - 虚拟模拟资金，仅供学习和测试
> - 🎯 **适用场景** - 投资学习、策略测试、模拟交易

## ✨ 功能特性

| 功能 | 说明 |
|------|------|
| 📝 账户管理 | 注册、切换、查看账户列表 |
| 📊 基金查询 | 查询基金列表、详情、推荐基金 |
| 💰 交易操作 | 申购、赎回、撤销订单 |
| 📈 资产查询 | 持仓、收益、交易记录 |
| 🔐 安全认证 | OAuth 2.0 + JWT Token 自动刷新 |
| 💾 数据持久化 | 本地配置文件存储账户信息 |

## 📦 安装

### Python 版本 (PyPI)

```bash
# 全局安装
pip install fund-trading-skill

# 使用国内镜像
pip install fund-trading-skill -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### TypeScript 版本 (npm)

```bash
# 全局安装
npm install -g fund-trading-skill

# 使用国内镜像
npm install -g fund-trading-skill --registry=https://registry.npmmirror.com
```

## 🚀 快速开始

### 1. 注册账户

首次使用需要注册账户：

```bash
fund-trading register --username 我的账户
```

输出：

```
🔄 正在注册账户: 我的账户...
✅ 注册成功!
   账户名: 我的账户
   MEMBER_ID: FC20260330XXXX
   CLIENT_ID: xxxxxxxx
   CLIENT_SECRET: xxxxxxxx

📌 已自动切换到新账户
```

### 2. 查询持仓

```bash
fund-trading position
```

输出：

```
┌──────────────────────────────────────────────────┐
│                   💰 资产概览                      │
├──────────────────────────────────────────────────┤
│  总资产: 10000.00元                               │
│  总收益: 📈 +200.00元 (+2.00%)                    │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│                            📊 持仓明细                                │
├──────────────────────────────────────────────────────────────────────┤
│ 基金代码   名称                    份额         市值         │
├──────────────────────────────────────────────────────────────────────┤
│ 000001    华夏成长证券投资基金      1000.00份   10000.00元  │
└──────────────────────────────────────────────────────────────────────┘
```

### 3. 申购基金

```bash
fund-trading subscribe --fund-code 000001 --amount 1000
```

### 4. 查询交易记录

```bash
fund-trading orders
```

## 📋 完整命令

### 账户管理

```bash
fund-trading register --username <name>    # 注册新账户
fund-trading account --list                # 查看账户列表
fund-trading account --switch <member_id>  # 切换账户
fund-trading refresh-token                 # 刷新 Token
```

### 基金查询

```bash
fund-trading list                          # 查询基金列表
fund-trading detail --fund-code <code>     # 查询基金详情
fund-trading recommend                     # 获取推荐基金
```

### 交易操作

```bash
fund-trading position                      # 查询持仓
fund-trading orders                        # 查询交易记录
fund-trading subscribe --fund-code <code> --amount <金额>  # 申购
fund-trading redeem --fund-code <code> --shares <份额>     # 赎回
fund-trading cancel --trade-id <订单号>                     # 撤单
```

## 🔧 配置说明

### 配置文件位置

```
~/.config/opencode/skills/fund-trading/data/config.json
```

### 配置文件结构

```json
{
  "current_member_id": "FC20260330XXXX",
  "accounts": [
    {
      "member_id": "FC20260330XXXX",
      "username": "我的账户",
      "client_id": "xxxxxxxx",
      "client_secret": "xxxxxxxx",
      "created_at": "2026-03-30 10:00:00"
    }
  ],
  "tokens": {
    "xxxxxxxx": {
      "access_token": "eyJhbGci...",
      "expires_at": 1712592000
    }
  }
}
```

## 🔐 认证方式

使用 **OAuth 2.0 Client Credentials** 模式：

1. 调用 `/openapi/v1/oauth/token` 获取 JWT Token
2. 使用 `Authorization: Bearer {token}` 调用业务 API
3. Token 自动缓存，过期前 5 分钟自动刷新

## 📡 API 端点

| 功能 | API 路径 | 方法 |
|------|----------|------|
| Token | `/openapi/v1/oauth/token` | POST |
| 注册 | `/openapi/v1/channel/register` | POST |
| 基金列表 | `/openapi/v1/shipan/fund/list` | GET |
| 基金详情 | `/openapi/v1/shipan/fund/detail` | GET |
| 持仓查询 | `/openapi/v1/shipan/asset/query` | POST |
| 交易查询 | `/openapi/v1/shipan/trade/query` | POST |
| 申购 | `/openapi/v1/shipan/trade/subscribe` | POST |
| 赎回 | `/openapi/v1/shipan/trade/redeem` | POST |
| 撤单 | `/openapi/v1/shipan/trade/cancel` | POST |

## ❓ 故障排除

### 连接失败

**错误**: `Connection error: Connection refused`

**解决**: 确认 OpenAPI 服务已启动，检查端口是否正确

### Token 过期

**错误**: `401 Unauthorized`

**解决**: 运行 `fund-trading refresh-token`

### 命令未找到

**错误**: `command not found: fund-trading`

**解决**:
```bash
# Python
pip install --upgrade fund-trading-skill

# npm
npm update -g fund-trading-skill
```

## 📄 许可证

[MIT License](LICENSE)

## 👤 作者

**weiqitong**
- Email: weiqitong@nicaifu.com

## 🔗 相关链接

- [PyPI 包](https://pypi.org/project/fund-trading-skill/)
- [npm 包](https://www.npmjs.com/package/fund-trading-skill)
- [安装手册](./INSTALL.md)