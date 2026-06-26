# 历史日K行情数据

> 分类: 行情数据 | 目录: `行情数据` | 索引见 `SKILL.md`

<!-- generated_at: 2026-04-30T09:29:07.184-1777512547186 -->


### 描述

查询个股历史日K线行情数据，支持指定多只股票和日期范围（最长1年），返回每日开盘价、收盘价、最高价、最低价、成交量、成交额、涨跌幅等。适用于技术分析和历史走势复盘

### 请求参数

| 名称 | 类型 | 必填 | 默认值 | 说明 |
|:---|:---|:---|:---|:---|
| `interfaceId` | `str` | 是 | "G2" | 接口ID |
| `stockCodes` | `str` | 是 | - | 支持查询单只股票和多只股票（单次查询不超过20个），如果是多只，以逗号隔开；示例：'000001',<br>'600519' |
| `startDate` | `str` | 否 | - | 开始日期 startDate和endDate区间不能超过一年，如超过数据会截断，如果都为空，<br>则查询最新交易日，示例：2023-01-01 |
| `endDate` | `str` | 否 | - | 结束日期 startDate和endDate区间不能超过一年，如超过数据会截断，如果都为空，<br>则查询最新交易日，示例：2023-12-31 |

### 返回参数

ResultData.data 为 List，元素为历史日K行情列表

| 名称 | 类型 | 是否必返回 | 说明 |
|:---|:---|:---|:---|
| `stockCode` | `str` | 否 | 股票代码 |
| `stockName` | `str` | 否 | 股票名称 |
| `tradeDate` | `str` | 否 | 交易日 |
| `newPrice` | `float` | 否 | 最新价 |
| `maxPrice` | `float` | 否 | 最高价 |
| `minPrice` | `float` | 否 | 最低价 |
| `openPrice` | `float` | 否 | 开盘价 |
| `yesterdayClosePrice` | `float` | 否 | 昨收价 |
| `chg` | `float` | 否 | 涨跌幅 |
| `chgMoney` | `float` | 否 | 涨跌额 |
| `volume` | `int` | 否 | 成交量 |
| `tradeMoney` | `float` | 否 | 成交额 |
| `turnoverRate` | `float` | 否 | 换手率 |
| `quantityRelative` | `float` | 否 | 量比 |
| `marketValue` | `float` | 否 | 市值 |
| `circulateMarketValue` | `float` | 否 | 流通市值 |
| `indicatorResponse` | `IndicatorResponse` | 否 | 技术指标 |
| `macd` | `list[MacdIndicator]` | 否 | MACD指标 |
| `kdj` | `list[KdjIndicator]` | 否 | KDJ指标 |
| `boll` | `list[BollIndicator]` | 否 | BOLL指标 |
| `rsi` | `list[RsiIndicator]` | 否 | RSI指标 |
| `turnover` | `list[TurnoverIndicator]` | 否 | 换手率指标 |
| `ma5` | `list[MAIndicator]` | 否 | 5日均线指标 |
| `ma10` | `list[MAIndicator]` | 否 | 10日均线指标 |

**`macd`** 数组元素结构：

| 名称 | 类型 | 是否必返回 | 说明 |
|:---|:---|:---|:---|
| `dateTime` | `ZonedDateTime` | 否 | 时间 |
| `macd` | `float` | 否 | MACD值 |
| `signal` | `float` | 否 | 信号值 |
| `histogram` | `float` | 否 | 直方图值 |
| `shortPeriod` | `int` | 否 | 短周期 |
| `longPeriod` | `int` | 否 | 长周期 |
| `signalPeriod` | `int` | 否 | 信号周期 |

**`kdj`** 数组元素结构：

| 名称 | 类型 | 是否必返回 | 说明 |
|:---|:---|:---|:---|
| `dateTime` | `ZonedDateTime` | 否 | 时间 |
| `k` | `float` | 否 | K值 |
| `d` | `float` | 否 | D值 |
| `j` | `float` | 否 | J值 |
| `n` | `int` | 否 | K值周期 |
| `m1` | `int` | 否 | J值周期 |
| `m2` | `int` | 否 | D值周期 |

**`boll`** 数组元素结构：

| 名称 | 类型 | 是否必返回 | 说明 |
|:---|:---|:---|:---|
| `dateTime` | `ZonedDateTime` | 否 | 时间 |
| `upper` | `float` | 否 | 上轨值 |
| `middle` | `float` | 否 | 中轨值 |
| `lower` | `float` | 否 | 下轨值 |
| `period` | `int` | 否 | 周期 |

**`rsi`** 数组元素结构：

| 名称 | 类型 | 是否必返回 | 说明 |
|:---|:---|:---|:---|
| `dateTime` | `ZonedDateTime` | 否 | 时间 |
| `rsi` | `float` | 否 | RSI值 |
| `period` | `int` | 否 | 周期 |

**`turnover`** 数组元素结构：

| 名称 | 类型 | 是否必返回 | 说明 |
|:---|:---|:---|:---|
| `dateTime` | `ZonedDateTime` | 否 | 时间 |
| `turnover` | `float` | 否 | 换手率值 |
| `period` | `int` | 否 | 周期 |

**`ma5`** 数组元素结构：

| 名称 | 类型 | 是否必返回 | 说明 |
|:---|:---|:---|:---|
| `dateTime` | `ZonedDateTime` | 否 | 时间 |
| `value` | `float` | 否 | MA值 |
| `period` | `int` | 否 | 周期 |

**`ma10`** 数组元素结构：

| 名称 | 类型 | 是否必返回 | 说明 |
|:---|:---|:---|:---|
| `dateTime` | `ZonedDateTime` | 否 | 时间 |
| `value` | `float` | 否 | MA值 |
| `period` | `int` | 否 | 周期 |

### 调用示例

```python
from equal_data import EqualDataApi  
api = EqualDataApi('your API_KEY') 
# 调用接口
data = api.query_equal_data(
    interfaceId="G2",
    stockCodes=None,  # str  # 默认: 
    startDate=None,  # str  # 默认: 
    endDate=None,  # str  # 默认: 
)
```


