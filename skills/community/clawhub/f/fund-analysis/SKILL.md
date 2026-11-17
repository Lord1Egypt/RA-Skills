---
name: fund-analysis
version: 1.1.0
description: "Analyze mutual fund performance, holdings, risk metrics, and investment suitability"
tags: [analysis, data, report-generation, visual, cli]
---

# 基金分析与金融数据工具包 v1.1

整合�?fund-daily-report �?financial-analysis-toolkit 两个技能，提供完整的基金市场和金融数据分析能力�?
## 什么时候使�?
- 用户要求生成基金日报
- 用户要求查看基金净值排�?涨幅排行
- 用户要求分析基金资金流向
- 用户要求查看行业资金�?- 用户要求查看基金加仓/减仓股票
- 用户要求分析个股基本面（PE/PB/ROE等）
- 用户要求分析行业/板块
- 用户要求查看宏观数据（LPR/CPI/PPI/PMI�?- 用户要求查看市场概览（成交额/北向资金/涨跌家数�?- 用户提到"天天基金"�?基金排行"�?基金日报"

## 核心能力

### 能力1：基金日报生�?
基于天天基金�?(fund.eastmoney.com) 和东方财富数据，生成基金市场分析报告�?
**报告包含4个板�?*�?
#### 板块1：过�?0天净值涨幅最高的10只基�?- 数据来源：`fund_open_fund_rank_em`（开放式基金�? `fund_exchange_rank_em`（场内ETF�?- 筛选：股票�?+ 混合�?+ 场内ETF，合并后统一排序
- 输出字段：基金代�?| 基金简�?| 单位净�?| �?月涨�?| 日增长率 | 基金类型

#### 板块2：过�?0天资金流入最多的10只基�?- 数据来源：`fund_exchange_rank_em`（场内ETF基金排行�?- 输出字段：基金代�?| 基金简�?| 单位净�?| �?月涨�?| �?月涨�?
#### 板块3：过�?0天资金流入最多的5个行�?- 数据来源：`stock_fund_flow_concept`（概念板块资金流�?- 输出字段：行业名�?| 涨跌�?| 流入资金 | 流出资金 | 净流入

#### 板块4：过�?0天基金加仓最多的10只股�?- 数据来源：`stock_zh_a_spot_em`（A股实时行情）
- 输出字段：股票代�?| 股票名称 | 最新价 | 涨跌�?| 成交�?| 换手�?
**运行方式**�?```bash
cd skills/fund-analysis
python fund_daily_report.py
```

### 能力2：金融数据分析工具包

基于 AKShare + pywencai 实现金融数据获取和分析�?
#### 1. 个股基本面分�?- PE/PB/ROE/毛利�?净利率
- 营收/利润增长趋势
- 市值与行业对比

**数据接口**�?```python
import akshare as ak
# 财务报表
df = ak.stock_yjbb_em(date="20240331")
# 个股估�?df = ak.stock_individual_info_em(symbol="000001")
```

#### 2. 技术面分析
- �?K 线数据获�?- 均线系统（MA5/10/20/60�?- MACD/KDJ/RSI 指标计算

**数据接口**�?```python
import akshare as ak
# A股日K�?df = ak.stock_zh_a_hist(symbol="000001", period="daily")
# 指数日K�?df = ak.stock_zh_index_daily(symbol="sh000001")
```

#### 3. 行业分析
- 行业资金流向（pywencai�?- 板块涨跌幅排�?- 行业估值对�?
**数据接口**�?```python
import pywencai
# 行业资金�?res = pywencai.get(query="今日行业资金流入�?0")
```

#### 4. 宏观分析
- LPR/利率数据
- CPI/PPI
- PMI 数据

**数据接口**�?```python
import akshare as ak
# LPR
df = ak.macro_china_lpr()
# CPI
df = ak.macro_china_cpi()
# PPI
df = ak.macro_china_ppi()
# PMI
df = ak.macro_china_pmi()
```

#### 5. 市场概览
- 沪深两市成交�?- 北向资金流向
- 涨跌家数�?
**数据接口**�?```python
import akshare as ak
# 北向资金
df = ak.stock_hsgt_north_net_flow_in_em()
# A股实时行情（涨跌统计�?df = ak.stock_zh_a_spot_em()
```

## 数据源架�?
| 数据需�?| 数据�?| 工具 | 状�?|
|---------|--------|------|------|
| 基金排行 | 天天基金/东方财富 | AKShare | 可用 |
| A 股行�?| AKShare | `ak.stock_zh_a_hist()` | 可用 |
| 指数行情 | AKShare | `ak.stock_zh_index_daily()` | 可用 |
| 财务报表 | AKShare | `ak.stock_yjbb_em()` | 可用 |
| 自然语言选股 | pywencai | `pywencai.get()` | 可用 |
| 宏观数据 | AKShare | `ak.macro_china_*()` | 可用 |
| 个股估�?| AKShare | `ak.stock_individual_info_em()` | 可用 |

## 错误处理与降级策�?
### 数据源故�?| 场景 | 处理方式 |
|------|---------|
| AKShare 接口超时 | 等待 5s 重试 1 �?�?提示用户稍后重试 |
| AKShare 返回空数�?| 检查是否非交易时间 �?提示"非交易时段，数据将在下一交易日更�? |
| pywencai 查询失败 | 跳过问财数据，使�?AKShare 替代 |
| 东方财富接口被拦截（403�?| 自动降级�?AKShare 接口 |
| 天天基金网数据延�?| 标注数据更新时间，提�?T+1 数据，非实时" |
| 所有数据源均失�?| 输出明确错误 + 建议检查网�?+ 提供上次缓存结果（如有） |

### 数据质量
| 场景 | 处理方式 |
|------|---------|
| 基金净值为 0 �?NaN | 跳过该基金，标注"数据异常" |
| 涨跌幅超�?±100% | 标注为异常值，不纳入排�?|
| 行业分类缺失 | 归入"未分�?，不影响其他行业统计 |

### 执行时段建议
- 交易�?15:30 后执行：数据最完整
- 交易�?9:30-15:00：盘中数据，标注"盘中实时"
- 非交易日：提�?非交易日"，展示最近交易日数据

## 依赖

```bash
pip install akshare pywencai pandas numpy
```

## AKShare 接口清单

| 用�?| 接口 | 状�?|
|------|------|------|
| 开放式基金排行 | `fund_open_fund_rank_em` | 可用 |
| ETF基金排行 | `fund_exchange_rank_em` | 可用 |
| 概念板块资金�?| `stock_fund_flow_concept` | 可能被拦�?|
| A股实时行�?| `stock_zh_a_spot_em` | 可能被拦�?|
| A股日K�?| `stock_zh_a_hist` | 可用 |
| 财务报表 | `stock_yjbb_em` | 可用 |
| 个股信息 | `stock_individual_info_em` | 可用 |
| 宏观数据 | `macro_china_*` | 可用 |

## 注意事项

- 净值数据：T+1（每日更新）
- 资金流数据：实时
- 建议基金日报执行时间：每个交易日 15:30 之后
- 部分东方财富接口可能被拦截，自动降级�?AKShare

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.1.0 | 2026-06-29 | 增加错误处理、降级策略、依赖声明、修复接口名�?|
| 1.0.0 | 2026-06-20 | 合并 fund-daily-report + financial-analysis-toolkit |
