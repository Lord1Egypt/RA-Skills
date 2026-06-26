---
name: fiu-market-assistant
description: "FIU MCP 行情交易助手。当用户想要查询股票行情、K线、交易股票、查看持仓或分析港股/美股/A股市场数据时使用。"
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash
metadata:
  openclaw:
    requires:
      env:
        - FIU_MCP_TOKEN
      binaries:
        - curl
        - jq
        - date
        - bash
      primaryCredential: FIU_MCP_TOKEN
---

# /fiu-market-assistant — FIU 行情交易助手

通过 FIU MCP Server 提供股票市场数据查询和交易功能。支持港股、美股、A股的行情、K线、买卖盘、资金流向和交易操作。

参数传递: `$ARGUMENTS`

---

## 快速开始（一步配置）

```bash
# 首次配置 - 设置 MCP 和 Token
/fiu-market-assistant setup 你的_FIU_MCP_TOKEN
```

配置完成后，直接用自然语言提问：
```
查询腾讯控股行情
显示苹果日K线
买入100股腾讯
```

---

## 命令 dispatch

### 无参数 — 显示状态

1. **检查 FIU_MCP_TOKEN** - 显示是否已配置（脱敏）
2. **显示可用市场** - 列出 HK, US, CN, toolkit
3. **显示快速命令** - 列出可用的 dispatch 命令
4. **下一步** - 引导用户：
   - 未配置 → "运行 `/fiu-market-assistant setup <token>` 进行配置"
   - 已配置 → "就绪! 可以提问如 '查询00700行情'"

### `setup <token>` — 快速配置（推荐）

1. 保存 token 到配置文件 `~/.fiu-market/config`
2. 创建 MCP 配置文件 `.mcp.json`，包含全部 7 个 FIU 服务
3. 测试连接
4. 确认并引导重启

### `test` — 测试连接

1. 检查 FIU_MCP_TOKEN 是否已设置
2. 用 tools/list 测试每个市场端点
3. 显示哪些服务可用
4. 报告错误

### `discover <market>` — 发现可用工具

列出特定市场的所有可用工具：

```
/fiu-market-assistant discover hk_sdk
/fiu-market-assistant discover cn_sdk
```

### `quote <股票代码>` — 查询行情

查询股票实时行情：

```
/fiu-market-assistant quote 00700
/fiu-market-assistant quote AAPL
/fiu-market-assistant quote 600519
```

### `kline <股票代码> [类型]` — 查询K线

查询K线数据：

```
/fiu-market-assistant kline 00700        # 日K
/fiu-market-assistant kline 00700 1      # 周K
/fiu-market-assistant kline AAPL 5       # 美股1分钟K
```

### `search <关键词>` — 搜索股票代码

按名称搜索股票：

```
/fiu-market-assistant search 腾讯
/fiu-market-assistant search Apple
```

### `trade <操作> <股票代码> <数量> [价格]` — 交易

下单（默认模拟模式）：

```
/fiu-market-assistant trade buy 00700 100 380
/fiu-market-assistant trade sell AAPL 50 150
/fiu-market-assistant trade buy 600519 1000 200
```

### `positions` — 查询持仓

```
/fiu-market-assistant positions
```

### `cash` — 查询资金

```
/fiu-market-assistant cash
```

### `orders` — 查询订单

```
/fiu-market-assistant orders
```

### `capflow <股票代码>` — 资金流向

```
/fiu-market-assistant capflow 00700
```

---

## MCP 服务器参考

### 市场端点

| 服务 | 市场 | URL |
|------|------|-----|
| stockHkF10 | 港股F10 | https://ai.szfiu.com/stock_hk_f10/ |
| stockUsF10 | 美股F10 | https://ai.szfiu.com/stock_us_f10/ |
| stockCnF10 | A股F10 | https://ai.szfiu.com/stock_cn_f10/ |
| stockHkSdk | 港股SDK | https://ai.szfiu.com/stock_hk_sdk/ |
| stockUsSdk | 美股SDK | https://ai.szfiu.com/stock_us_sdk/ |
| stockCnSdk | A股SDK | https://ai.szfiu.com/stock_cn_sdk/ |
| szfiuToolkit | 代码检索 | https://ai.szfiu.com/toolkit/ |

### 各市场功能支持

| 功能 | 港股 | 美股 | A股 |
|------|------|------|-----|
| 行情 | ✅ | ✅ | ✅ |
| K线 | ✅ | ✅ | ✅ |
| 买卖盘 | ✅ | ✅ | ✅ |
| 逐笔成交 | ✅ | ✅ | ✅ |
| 分时数据 | ✅ | ✅ | ✅ |
| 资金流向 | ✅ | ✅ | ✅ |
| 资金分布 | ✅ | ✅ | ✅ |
| 板块列表 | ✅ | ✅ | ✅ |
| 条件选股 | ✅ | ✅ | ✅ |
| 市场排行榜 | ✅ | ✅ | ✅ |
| F10数据 | ✅ | ✅ | ✅ |
| 交易功能 | ✅ | ✅ | ✅ |
| 代码搜索 | ✅ | ✅ | ✅ |

---

## 使用技巧

1. **先用 search** 找到正确的股票代码
2. **默认模式是模拟交易** - 使用 "REAL" 进行实盘
3. **港股**: 使用格式 `00700.HK` 或直接 `00700`
4. **美股**: 使用格式 `AAPL` 或 `AAPL.US`
5. **A股**: 使用格式 `600519.SZ` 或 `000001.SZ`
6. **限频**: 30秒内最多15笔订单
7. **获取Token**: https://ai.szfiu.com/auth/login

## 重要提示

- 交易默认使用模拟模式，安全第一
- 实盘交易需要明确确认 "REAL"
- 交易前请先检查市场是否开市
- setup 命令会创建/覆盖 ~/.mcp.json（标准 MCP 配置文件）
- 覆盖前会自动创建备份
- 配置文件权限设置为 600，仅所有者可读
- 此技能会向您的 MCP 配置添加 7 个 FIU MCP 条目
- 其他 MCP 工具也可能使用 ~/.mcp.json，如需要请在设置后检查