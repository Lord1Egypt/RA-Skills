---
name: akshare-stock
description: 使用 AkShare 库获取 A股、港股、美股的股票数据，包括实时行情、历史行情、财务数据、股东数据、资金流向、板块数据、龙虎榜、融资融券、新股IPO、大宗交易、估值指标、ESG评级等。当用户需要查询股票行情、获取股票数据、分析股票财务信息、查看龙虎榜、了解资金流向、获取板块数据时使用此 skill。
---

# AkShare 股票数据 Skill

## 概述

使用 Python AkShare 库获取股票数据。所有数据通过 `exec` 运行 Python 脚本获取，结果以 CSV/JSON 格式返回。

**环境要求**: Python 3.11+, 已安装 `akshare` 库

## 快速开始

### 使用辅助脚本（推荐）

脚本路径: `skills/akshare-stock/scripts/stock_data.py`

```bash
# 实时行情
python3 skills/akshare-stock/scripts/stock_data.py spot
python3 skills/akshare-stock/scripts/stock_data.py spot-sh    # 沪A
python3 skills/akshare-stock/scripts/stock_data.py spot-sz    # 深A
python3 skills/akshare-stock/scripts/stock_data.py spot-cy    # 创业板
python3 skills/akshare-stock/scripts/stock_data.py spot-kc    # 科创板
python3 skills/akshare-stock/scripts/stock_data.py spot-us    # 美股
python3 skills/akshare-stock/scripts/stock_data.py spot-hk    # 港股

# 历史行情 (symbol, start, end, period, adjust)
python3 skills/akshare-stock/scripts/stock_data.py hist 600519 20250101 20250522 daily qfq

# 分时历史 (symbol, period_min, start_date, end_date, adjust)
python3 skills/akshare-stock/scripts/stock_data.py hist-min 600519 5 20250501 20250522 qfq

# 日内分时
python3 skills/akshare-stock/scripts/stock_data.py intraday 600519

# 个股信息
python3 skills/akshare-stock/scripts/stock_data.py info 600519
python3 skills/akshare-stock/scripts/stock_data.py info-xq SH600519

# 行情报价
python3 skills/akshare-stock/scripts/stock_data.py bid-ask 600519

# 财务报表 (symbol, report_type, period_type)
python3 skills/akshare-stock/scripts/stock_data.py financial 600519 balance report
python3 skills/akshare-stock/scripts/stock_data.py financial 600519 profit quarterly
python3 skills/akshare-stock/scripts/stock_data.py financial 600519 cashflow yearly

# 财务指标
python3 skills/akshare-stock/scripts/stock_data.py financial-indicator 600519

# 十大股东 / 十大流通股东
python3 skills/akshare-stock/scripts/stock_data.py top10 600519
python3 skills/akshare-stock/scripts/stock_data.py top10-free 600519

# 资金流向
python3 skills/akshare-stock/scripts/stock_data.py fund-flow 600519
python3 skills/akshare-stock/scripts/stock_data.py fund-flow-rank

# 板块数据
python3 skills/akshare-stock/scripts/stock_data.py board-concept
python3 skills/akshare-stock/scripts/stock_data.py board-concept-spot
python3 skills/akshare-stock/scripts/stock_data.py board-concept-cons 人工智能
python3 skills/akshare-stock/scripts/stock_data.py board-industry
python3 skills/akshare-stock/scripts/stock_data.py board-industry-spot
python3 skills/akshare-stock/scripts/stock_data.py board-industry-cons 半导体

# 涨停股池
python3 skills/akshare-stock/scripts/stock_data.py zt-pool

# 龙虎榜 (date: YYYYMMDD)
python3 skills/akshare-stock/scripts/stock_data.py lhbcg 20260522

# 融资融券
python3 skills/akshare-stock/scripts/stock_data.py margin-sse
python3 skills/akshare-stock/scripts/stock_data.py margin-szse

# 股票热度
python3 skills/akshare-stock/scripts/stock_data.py hot-rank

# 历史分红
python3 skills/akshare-stock/scripts/stock_data.py dividend 600519

# 历史分笔
python3 skills/akshare-stock/scripts/stock_data.py tick 600519
```

### 直接编写 Python 代码

对于脚本未覆盖的接口，直接编写 Python 代码执行:

```python
import akshare as ak
import pandas as pd

# 示例: 获取实时行情
df = ak.stock_zh_a_spot_em()
print(df.to_csv(index=False))

# 示例: 获取历史行情
df = ak.stock_zh_a_hist(symbol="600519", period="daily", 
                         start_date="20250101", end_date="20250522", 
                         adjust="qfq")
print(df.to_csv(index=False))
```

## 常用接口速查

### 股票代码格式
- A股: `600519` (数字格式)
- 雪球: `SH600519` (带前缀)
- 港股: `00700`
- 美股: `AAPL`

### 复权参数
- `""` 不复权
- `"qfq"` 前复权 (推荐)
- `"hfq"` 后复权

### 周期参数
- `"daily"` 日频
- `"weekly"` 周频
- `"monthly"` 月频

## 完整接口列表

详见 [references/api_reference.md](references/api_reference.md)，包含 372 个接口的完整文档。

### 主要分类

| 分类 | 常用接口数 | 说明 |
|------|-----------|------|
| A股实时行情 | 10 | 沪深京A股、创业板、科创板、B股等 |
| A股历史行情 | 14 | 日/周/月频、分时、盘前数据 |
| 个股信息 | 5 | 东财/雪球个股基本信息 |
| 财务数据 | 20+ | 资产负债表、利润表、现金流量表、财务指标 |
| 股东数据 | 20+ | 十大股东、流通股东、股东增减持、持股分析 |
| 资金流向 | 13 | 个股/板块/行业/概念资金流、主力净流入 |
| 板块数据 | 15+ | 概念板块、行业板块、板块成份、板块行情 |
| 市场热点 | 15+ | 涨停/跌停/强势/炸板股池、股票热度、龙虎榜 |
| 融资融券 | 8 | 上交所/深交所融资融券汇总与明细 |
| 美股数据 | 8 | 实时/历史行情、财务数据、粉单市场 |
| 港股数据 | 15+ | 实时/历史行情、财务数据、行业对比 |
| 沪深港通 | 15+ | 港股通成份股、资金流向、持股数据 |
| 新股IPO | 15+ | 打新收益率、申购中签、IPO审核、增发配股 |
| 大宗交易 | 8 | 市场统计、每日明细、活跃营业部 |
| 估值指标 | 15+ | 市盈率、市净率、股息率、巴菲特指标 |
| ESG评级 | 5 | MSCI、路孚特、秩鼎、华证指数 |

## 注意事项

1. **新浪接口易封IP**: `stock_zh_a_spot()`, `stock_zh_a_daily()`, `stock_zh_a_minute()` 等新浪数据源接口调用频率过高会被封IP，优先使用东财接口
2. **数据延迟**: 港股/美股数据可能有15分钟延迟
3. **交易时间**: 实时行情在交易时间内(9:30-15:00)更新，盘后数据需等收盘
4. **数据量**: 全量实时行情返回2000+条数据，建议按需筛选
5. **日期格式**: 大部分接口使用 `YYYYMMDD` 格式，部分使用 `YYYY-MM-DD`
