---
name: cn-funds-mcp
description: >-
  China fund & stock data assistant (free API, no API key required). Query fund valuation,
  NAV, holdings, manager info, stock/index quotes, market capital flow, sector ranking,
  northbound capital, and manage user's fund portfolio with profit calculation via cn-funds-mcp tools.
  中国基金/股票数据查询助手。使用 cn-funds-mcp 工具查询基金估值、净值、持仓、经理信息，
  查询股票/指数行情，查看大盘资金流向、板块排行、北向资金，以及管理用户的基金持仓并计算收益。
  当用户提及基金、股票、大盘、持仓、收益、净值、估值、北向资金等关键词时使用。
---

# cn-funds-mcp 使用指南

## 工具速查

### 基金查询

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| `search_fund` | 搜索基金（名称/代码/拼音） | `keyword` |
| `get_fund_estimate` | 实时估值（盘中估算净值和涨跌幅） | `fundCode` |
| `get_fund_batch_info` | 批量获取多只基金净值 | `fundCodes`（逗号分隔） |
| `get_fund_info` | 基金详情（类型/公司/经理/规模/排名） | `fundCode` |
| `get_fund_valuation_detail` | 当日估值走势（日内分时） | `fundCode` |
| `get_fund_net_value_history` | 历史净值走势 | `fundCode`, `range` |
| `get_fund_accumulated_performance` | 累计收益 vs 沪深300 vs 同类 | `fundCode`, `range` |
| `get_fund_position` | 持仓股票明细 | `fundCode` |
| `get_fund_manager_list` | 历任经理列表 | `fundCode` |
| `get_fund_manager_detail` | 现任经理简介 | `fundCode` |

### 股票/指数

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| `get_stock_trend` | 日内分时走势 | `secid`（如 `1.600519`） |
| `get_stock_quote` | 实时行情报价 | `secids`（逗号分隔） |

### 大盘/资金

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| `get_market_overview` | A股大盘概况（上证/深证） | 无 |
| `get_market_capital_flow` | 大盘资金流向（主力/大小单） | 无 |
| `get_sector_capital_flow` | 板块资金排行 | `timeType`, `code` |
| `get_northbound_capital` | 沪深港通资金流向 | 无 |

### 持仓管理

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| `save_portfolio` | 保存/更新持仓记录 | `fundCode`, `shares`, `costPrice` |
| `remove_portfolio` | 删除持仓记录 | `fundCode` |
| `get_portfolio` | 查看持仓列表 | 无 |
| `get_portfolio_profit` | 一键查询今日收益和总收益 | 无 |

### 定时提醒

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| `set_reminder` | 设置定时提醒（每个交易日触发） | `time`(HH:MM), `type`, `message` |
| `get_reminders` | 查看所有提醒设置 | 无 |
| `remove_reminder` | 删除某个提醒 | `id` |
| `check_reminders` | 检查是否有到期提醒 | 无 |

提醒类型 `type`:
- `profit_report` — 持仓收益播报（触发后查询 `get_portfolio_profit`，给出加仓/减仓建议）
- `market_report` — 大盘行情播报（触发后查询大盘概况 + 资金流向）
- `custom` — 自定义提醒（配合 `message` 参数）

## 常用参数说明

**基金代码 `fundCode`**: 6 位数字，如 `161725`（招商白酒）、`110011`（易方达中小盘）

**证券ID `secid`**: 格式为 `市场.代码`

| 市场代码 | 含义 | 示例 |
|----------|------|------|
| `1.` | 上交所 | `1.000001`（上证指数）、`1.600519`（贵州茅台） |
| `0.` | 深交所 | `0.399001`（深证成指）、`0.000858`（五粮液） |
| `116.` | 港股 | `116.01810`（小米集团） |

**时间范围 `range`**: `m`=1月, `q`=3月, `hy`=6月, `y`=1年, `2y`=2年, `3y`=3年, `5y`=5年

## 主动行为（重要）

### 每次对话开始时，必须先调用 `check_reminders`

无论用户说了什么，在回复用户之前，**先调用 `check_reminders`** 检查是否有到期提醒。如果有到期提醒，按以下规则执行：

1. **`profit_report` 到期时**：
   - 调用 `get_portfolio_profit` 获取收益数据
   - 调用 `get_market_overview` 获取大盘背景
   - 以友好的语气向用户播报今日持仓收益总览
   - 对每只基金给出操作建议：
     - 今日跌幅 > 2%：提示"可考虑适当加仓摊低成本"
     - 今日涨幅 > 3%：提示"涨幅较大，可考虑部分止盈"
     - 持仓总亏损 > 10%：提示"亏损较大，建议评估是否继续持有"
     - 持仓总盈利 > 20%：提示"盈利可观，建议分批止盈锁定收益"
   - 最后询问用户是否需要调整持仓

2. **`market_report` 到期时**：
   - 调用 `get_market_overview` + `get_market_capital_flow` + `get_northbound_capital`
   - 播报大盘指数、资金流向、北向资金动态

3. **`custom` 到期时**：
   - 向用户展示自定义提醒内容

如果没有到期提醒，则正常处理用户的请求。

## 典型场景

### 用户不知道基金代码

先用 `search_fund` 搜索，再用返回的 `code` 调用其他工具。

### 用户问"今天大盘怎么样"

依次调用 `get_market_overview` + `get_market_capital_flow`，综合播报大盘点位、涨跌、成交额、资金流向。

### 用户问"我今天赚了多少"

直接调用 `get_portfolio_profit`，返回每只基金的今日收益和汇总。如果没有持仓记录，引导用户用 `save_portfolio` 添加。

### 用户告知持仓信息

解析出基金代码、份额、成本价，逐只调用 `save_portfolio` 保存。名称参数可省略，工具会自动查询填充。

### 用户想快速导入持仓（截图识别）

如果当前模型支持图片识别（OCR），主动提示用户：可以直接上传基金APP（如天天基金、支付宝、蚂蚁财富等）的持仓截图，AI 会自动识别图片中的基金代码、基金名称、持有份额、成本净值等信息，然后逐只调用 `save_portfolio` 批量导入持仓，无需手动逐个输入。

处理流程：
1. 识别截图中的每只基金信息（代码、份额、成本价）
2. 对于识别不完整的字段（如只有名称没有代码），用 `search_fund` 补全基金代码
3. 逐只调用 `save_portfolio` 保存
4. 保存完成后汇总展示已导入的持仓列表，并提示用户确认是否有遗漏或错误

### 用户问某只基金的全面分析

组合调用: `get_fund_info` + `get_fund_estimate` + `get_fund_position` + `get_fund_accumulated_performance`，从基本面、估值、持仓、历史收益多维度分析。

### 用户说"帮我设置每天下午提醒收益"

调用 `set_reminder`，参数 `time="14:30"`, `type="profit_report"`。之后每个交易日 14:30 后的首次对话会自动触发收益播报和操作建议。

### 提醒触发后的播报示例

> 下午好！现在是 14:30，为您播报今日持仓收益：
>
> 持仓总览：3 只基金，总成本 15000.00 元，当前市值 14520.00 元
> 今日收益：-180.00 元 | 持仓总收益：-480.00 元（-3.20%）
>
> 各基金明细：
> - 招商白酒A (161725)：今日 -1.22%，持仓亏损 -11.07%，建议评估是否继续持有
> - 易方达蓝筹 (005827)：今日 +0.35%，持仓盈利 +5.20%，继续持有
> - 广发纳斯达克 (270042)：今日 +1.80%，持仓盈利 +15.30%，走势良好
>
> 需要调整持仓吗？

## 注意事项

- 估值数据仅在 A 股交易时段（9:30-15:00）更新，非交易时段返回的是收盘数据
- `get_fund_estimate` 返回的是**估算值**，非最终净值，需提示用户
- 持仓数据持久化在 `data/portfolio.json`，跨会话保留
- 收益计算：今日收益 = 份额 ×（估值 - 昨日净值），持仓收益 = 份额 ×（估值 - 成本价）

## 作者

[smallke](https://github.com/smallke) | smallkes@qq.com
