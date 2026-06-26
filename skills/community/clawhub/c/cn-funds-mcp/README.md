# cn-funds-mcp

China fund & stock data MCP server powered by EastMoney free API. No API key required.

基金/股票数据 MCP 服务，基于东方财富(EastMoney) 免费 API 提供数据查询能力，无需配置 API Key，开箱即用。

**作者**: [smallke](https://github.com/smallke) | **邮箱**: smallkes@qq.com

## 截图预览 / Screenshots

| 持仓收益查询 | 定时收益播报 | 定时提醒设置 |
|:---:|:---:|:---:|
| ![持仓收益](screenshot/1.png) | ![收益播报](screenshot/2.png) | ![定时提醒](screenshot/3.png) |

## MCP 工具列表

### 基金相关

| 工具名                             | 说明                                                       | 参数                                                           |
| ---------------------------------- | ---------------------------------------------------------- | -------------------------------------------------------------- |
| `search_fund`                      | 根据关键词搜索基金（支持名称、代码、拼音缩写）             | `keyword` - 搜索关键词，如 `白酒`、`161725`                    |
| `get_fund_estimate`                | 获取基金实时估值数据（盘中估算净值和涨跌幅）               | `fundCode` - 基金代码，如 `161725`                             |
| `get_fund_batch_info`              | 批量获取多只基金的基本信息（净值、涨跌幅）                 | `fundCodes` - 基金代码，多个用逗号分隔                         |
| `get_fund_info`                    | 获取基金详细信息（类型、公司、经理、规模、近期收益排名等） | `fundCode` - 基金代码                                          |
| `get_fund_valuation_detail`        | 获取基金当日估值走势（日内分时估值变化数据）               | `fundCode` - 基金代码                                          |
| `get_fund_net_value_history`       | 获取基金历史净值走势（单位净值、累计净值）                 | `fundCode` - 基金代码；`range` - 时间范围（m/q/hy/y/2y/3y/5y） |
| `get_fund_accumulated_performance` | 获取基金累计收益走势，并与沪深300及同类平均对比            | `fundCode` - 基金代码；`range` - 时间范围                      |
| `get_fund_position`                | 获取基金股票持仓明细（持仓股票、占比、较上期变化）         | `fundCode` - 基金代码                                          |
| `get_fund_manager_list`            | 获取基金历任经理列表（任职起止日期、任职天数、任职涨幅）   | `fundCode` - 基金代码                                          |
| `get_fund_manager_detail`          | 获取基金现任经理详细信息（简历、照片、管理年限）           | `fundCode` - 基金代码                                          |

### 股票/指数相关

| 工具名            | 说明                                                 | 参数                                                                              |
| ----------------- | ---------------------------------------------------- | --------------------------------------------------------------------------------- |
| `get_stock_trend` | 获取股票或指数的日内分时走势数据                     | `secid` - 证券ID，格式 `市场.代码`，如 `1.000001`(上证指数)、`1.600519`(贵州茅台) |
| `get_stock_quote` | 获取股票或指数的实时行情报价（价格、涨跌幅、成交额） | `secids` - 证券ID列表，多个用逗号分隔                                             |

### 大盘/资金流向

| 工具名                    | 说明                                                                  | 参数                                                                    |
| ------------------------- | --------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `get_market_overview`     | 获取A股大盘概况（上证/深证的价格、涨跌、成交额、涨跌家数）            | 无                                                                      |
| `get_market_capital_flow` | 获取A股大盘当日资金流向（主力/超大单/大单/中单/小单净流入，单位亿元） | 无                                                                      |
| `get_sector_capital_flow` | 获取板块资金流向排行（行业板块或概念板块的资金净流入排名）            | `timeType` - 时间类型（f62=今日/f164=5日/f174=10日）；`code` - 板块筛选 |
| `get_northbound_capital`  | 获取沪深港通(北向/南向)资金实时流向数据（单位亿元）                   | 无                                                                      |

### 我的持仓

| 工具名 | 说明 | 参数 |
|--------|------|------|
| `save_portfolio` | 保存/更新基金持仓记录（已有则更新，没有则新增） | `fundCode` - 基金代码；`shares` - 持有份额；`costPrice` - 成本净值；`name` - 基金名称（可选） |
| `remove_portfolio` | 删除某只基金的持仓记录 | `fundCode` - 基金代码 |
| `get_portfolio` | 查看当前保存的所有基金持仓列表 | 无 |
| `get_portfolio_profit` | 一键查询所有持仓的今日收益和总收益（基于实时估值） | 无 |

持仓数据保存在 `data/portfolio.json` 文件中，格式示例：

```json
{
  "funds": [
    {
      "fundCode": "161725",
      "name": "招商中证白酒指数(LOF)A",
      "shares": 10000,
      "costPrice": 0.75,
      "updatedAt": "2026-03-18"
    }
  ]
}
```

`get_portfolio_profit` 返回每只基金的今日收益（估值 vs 昨日净值）、持仓总收益（估值 vs 成本净值）和收益率，以及汇总数据。

### 定时提醒

| 工具名 | 说明 | 参数 |
|--------|------|------|
| `set_reminder` | 设置定时提醒（每个交易日触发） | `time` - 时间(HH:MM)；`type` - 类型(profit_report/market_report/custom)；`message` - 自定义内容 |
| `get_reminders` | 查看所有提醒设置 | 无 |
| `remove_reminder` | 删除某个提醒 | `id` - 提醒ID |
| `check_reminders` | 检查是否有到期提醒（AI 每次对话开始时主动调用） | 无 |

提醒数据保存在 `data/reminders.json`，同一提醒每天只触发一次，周末自动跳过。

## 安装

```bash
npm install
```

## 使用

### 直接运行

```bash
npm start
```

### 在 Cursor 中配置

在 `.cursor/mcp.json` 中添加：

```json
{
  "mcpServers": {
    "cn-funds-mcp": {
      "command": "node",
      "args": ["src/index.js"],
      "cwd": "/path/to/cn-funds-mcp"
    }
  }
}
```

## 免责声明

本项目仅供学习和个人使用，不构成任何投资建议。所有基金、股票、指数等金融数据均来源于 [东方财富网（eastmoney.com）](https://www.eastmoney.com/)及其关联站点，数据版权归东方财富所有。本项目与东方财富无任何关联，亦未获得其官方授权。使用者应自行承担因使用本项目所产生的一切风险和责任。
