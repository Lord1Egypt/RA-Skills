---
name: agent-stock
description: 股市 AI 量化交易，用于获取股市实时数据、选股、交易决策、持仓分析、量化交易决策等。
author: AnoyiX
version: "0.2.8"
tags:
  - Stock
  - 股票数据
  - 选股
  - 持仓分析
  - 交易决策
  - 量化交易决策
---

# Agent Stock

帮助用户查询实时股市数据，分析数据，为用户提供交易决策。

## Workflows

当用户有如下需求时，可以查看对应的文档，帮用户完成相关任务：

- 短线交易选股：参考文档 [references/screen.md](references/screen.md)，为用户完成选股；
- 短线交易决策：参考文档 [references/trade.md](references/trade.md)，为用户完成个股交易决策；
- 短线量化交易决策：参考文档 [references/quant.md](references/quant.md)，为用户完成个股量化交易决策；
- 用户持仓分析：参考文档 [references/holdings.md](references/holdings.md)，为用户完成持仓分析；

## Prerequisites

检查 `stock` 命令是否已安装：

```bash
stock -v
```

如果没有安装，需要先安装 `stock` 命令行工具：

**uv:**
```bash
uv tool install agent-stock
```

**pip:**
```bash
pip3 install agent-stock
```

如果用户没有 `uv` 或者 `pip`，需要先帮用户安装好 python 环境，然后使用 `pip` 安装 `agent-stock` 包。