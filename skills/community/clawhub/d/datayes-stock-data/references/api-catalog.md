# Datayes API Catalog

按主题保存常用 `nameEn` 与高频参数。调用前仍然先用 `python scripts/datayes_api.py <nameEn> --spec-only` 获取最新规格，避免使用过期参数。日常查询建议加 `--result-only`；如果只想取单个字段，可再配合 `--field`。

## 行情数据

| 功能 | nameEn | 常用参数 |
|---|---|---|
| K线行情 | `market_HK` | `ticker`, `time`, `adjType`, `num`, `dateString`, `flag`, `type` |
| 盘口/实时快照 | `market_snapshot` | `ticker`, `type` |
| 当日分时行情 | `market_timeSharingDiagram` | `ticker`, `type=stock` |
| 5日分时走势 | `market_fiveDay_timeSharingDiagram` | `ticker`, `type=stock` |
| 区间涨跌统计 | `market_rang_statistics` | `ticker`, `beginDate`, `endDate`, `type=stock` |
| 技术面分析 | `market_tech_indic` | `ticker`, `beginDate`, `endDate` |
| 股票排行筛选 | `stock_ranking` | `type`, `sortKey`, `sortType`, `start`, `end`, `rangeMin`, `rangeMax` |
| 股票搜索 | `stock_search` | `query`, `dataType`, `topK` |

## 资金流向

| 功能 | nameEn | 常用参数 |
|---|---|---|
| 实时资金流向 | `stock_moneyflow_rt` | `ticker` |
| 历史每日资金 | `Ashare_money_flow_history` | `ticker`, `beginDate`, `endDate` |
| 按频率统计资金 | `Ashare_money_flow_freq` | `ticker`, `beginDate`, `endDate`, `statsFreq` |
| 当日实时流向 | `stock_current_moneyflow` | `ticker` |

## 财务报表

| 功能 | nameEn | 常用参数 |
|---|---|---|
| 利润表（累计） | `fdmt_is_new_lt` | `ticker`, `reportType`, `beginDate`, `endDate`, `field` |
| 利润表（单季） | `fdmt_is_new_q` | `ticker`, `reportType`, `beginDate`, `endDate`, `field` |
| 资产负债表 | `fdmt_bs_new_lt` | `ticker`, `reportType`, `beginDate`, `endDate`, `field` |
| 现金流量表 | `fdmt_cf_new_lt` | `ticker`, `reportType`, `beginDate`, `endDate`, `field` |
| 港股财务数据 | `hk_fdmt_fina_data` | `ticker` |

`reportType` 常用取值：`Q1` 一季报，`S1` 半年报，`Q3` 三季报，`A` 年报。

## 财务指标

| 功能 | nameEn | 常用参数 |
|---|---|---|
| 盈利能力（ROE/毛利率等） | `fdmt_indi_rtn` | `ticker`, `beginDate`, `endDate` |
| 营运能力（周转率等） | `fdmt_indi_trnovr` | `ticker`, `beginDate`, `endDate` |
| 成长能力（营收增速等） | `fdmt_indi_growth` | `ticker`, `beginDate`, `endDate` |
| 偿债能力 | `fdmt_indi_solvency` | `ticker`, `beginDate`, `endDate` |
| 每股指标（EPS等） | `fdmt_indi_ips` | `ticker`, `beginDate`, `endDate` |
| 主营业务占比 | `main_composition_ratio` | `ticker`, `beginDate`, `endDate` |
| 港股盈利能力 | `hk_fdmt_indi_rtn` | `ticker` |

## 估值与分析

| 功能 | nameEn | 常用参数 |
|---|---|---|
| 估值数据（PE/PB等） | `stock_evaluationAnalysis` | `ticker` |
| 机构持仓分析 | `stock_orgHolding` | `ticker` |
| 基本面分析 | `onepage_comment` | `ticker` |

## 常见映射

| 用户意图 | 首选接口 |
|---|---|
| “XX 现在多少钱” | `market_snapshot` |
| “XX 的净利润/营收” | `fdmt_is_new_lt` |
| “XX 的 ROE/毛利率” | `fdmt_indi_rtn` |
| “XX 资金流入” | `stock_moneyflow_rt` 或 `Ashare_money_flow_history` |
| “XX 最近 N 天 K 线” | `market_HK` |
| “PE 最低的股票” | `stock_ranking` |
| “XX 估值高不高” | `stock_evaluationAnalysis` |
| “机构持仓情况” | `stock_orgHolding` |
| “XX 区间涨幅” | `market_rang_statistics` |

## 注意事项

- `stock_search` 当前返回命中的代码字段是 `entity_id`，不是 `ticker`。
- `market_rang_statistics` 必须显式传 `type=stock`。
- 某些财务接口返回成功时用 `retCode: 1`，不要只检查 `code` 字段。
- `stock_ranking` 的字段名已变为 `sortKey` / `sortType` / `start` / `end`，不要再用旧的 `orderByField` / `orderType` / `pageSize` / `pageNum`。
- 当用户给的是公司名称而不是代码时，先调用 `stock_search` 再取 `entity_id` 或对应证券代码字段。
