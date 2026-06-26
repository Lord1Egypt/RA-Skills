---
name: ashareskill
description: 使用BaoStock获取股票K线数据及完整技术指标的专业工具。支持单只股票或股票池查询，支持自定义时间段和K线级别（日线/周线/月线），获取的数据包含均线、MACD、KDJ、RSI、BOLL、CCI等完整技术指标。适用于：1）获取股票历史K线数据用于策略回测；2）导出完整技术指标数据用于量化分析；3）批量获取多只股票数据。支持通过股票名称（如贵州茅台）或代码（如600519）查询A股所有股票。
---

# AShareSkill - A股数据获取工具

基于BaoStock数据源的股票数据分析工具，支持获取完整K线数据及各类技术指标。

## 功能特点

- **支持多种查询方式**：单只股票或股票池批量查询
- **灵活的时间段**：支持自定义起始和结束日期
- **多级别K线**：日线(d)、周线(w)、月线(m)
- **完整技术指标**：
  - 均线系统：MA5, MA10, MA20, MA30, MA60, MA120, MA250
  - MACD指标：DIF, DEA, MACD柱状
  - KDJ指标：K值, D值, J值
  - RSI指标：RSI6, RSI12, RSI24
  - 布林带(BOLL)：上轨, 中轨, 下轨
  - CCI指标
  - 成交量指标及涨跌幅数据
- **单一文件输出**：所有数据输出为一个CSV文件

## 使用方法

### 1. 直接调用脚本

```bash
# 单只股票查询
python kimi/ashareskill/scripts/ashareskill.py --stock 贵州茅台 --start 2023-01-01 --end 2024-01-01 --freq d

# 股票池查询（逗号分隔）
python kimi/ashareskill/scripts/ashareskill.py --stock "贵州茅台,中国平安,宁德时代" --start 2023-01-01 --end 2024-01-01

# 使用周线数据
python kimi/ashareskill/scripts/ashareskill.py --stock 600519 --start 2022-01-01 --freq w --output mydata.csv

# 使用月线数据
python kimi/ashareskill/scripts/ashareskill.py --stock 000001 --start 2020-01-01 --freq m

# 获取指数成分股（如中证500）月线数据
python kimi/ashareskill/scripts/ashareskill.py --index 000905 --start 2024-01-01 --freq m -o zz500.csv

# 获取沪深300成分股日线数据
python kimi/ashareskill/scripts/ashareskill.py --index 000300 --start 2024-01-01 --freq d -o hs300.csv
```

### 2. 参数说明

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--stock` | `-s` | 股票名称或代码（多只股票用逗号分隔） | 与--index二选一 |
| `--index` | `-i` | 指数代码，获取指数成分股（000905中证500，000300沪深300等） | 与--stock二选一 |
| `--start` |  | 开始日期 (YYYY-MM-DD) | 一年前 |
| `--end` |  | 结束日期 (YYYY-MM-DD) | 今天 |
| `--freq` | `-f` | K线级别: d(日线), w(周线), m(月线) | d |
| `--output` | `-o` | 输出文件名 | 自动生成 |
| `--adjust` | `-a` | 复权类型: 1(前复权), 2(后复权), 3(不复权) | 3 |

### 3. 作为Python模块使用

```python
from kimi.ashareskill.scripts.ashareskill import AShareSkill

# 创建实例
skill = AShareSkill()

# 获取单只股票数据
df = skill.get_kline_data(
    stock_code="sh.600519",  # 或 "贵州茅台"
    start_date="2023-01-01",
    end_date="2024-01-01",
    frequency="d"
)

# 获取多只股票数据
df_pool = skill.get_stock_pool_data(
    stock_list=["贵州茅台", "中国平安", "宁德时代"],
    start_date="2023-01-01",
    end_date="2024-01-01",
    frequency="d"
)

# 保存到文件
skill.save_to_csv(df_pool, "output.csv")
```

## 输出数据字段说明

| 字段名 | 说明 |
|--------|------|
| `code` | 股票代码 |
| `name` | 股票名称 |
| `date` | 交易日期 |
| `open` | 开盘价 |
| `high` | 最高价 |
| `low` | 最低价 |
| `close` | 收盘价 |
| `preclose` | 前收盘价 |
| `volume` | 成交量（股） |
| `amount` | 成交额（元） |
| `turn` | 换手率 |
| `pctChg` | 涨跌幅(%) |
| `peTTM` | 滚动市盈率 |
| `pbMRQ` | 市净率 |
| `psTTM` | 滚动市销率 |
| `pcfNcfTTM` | 滚动市现率 |
| `isST` | 是否ST股 |
| **均线指标** | |
| `ma5`, `ma10`, `ma20`, `ma30`, `ma60`, `ma120`, `ma250` | 各周期移动平均线 |
| **MACD指标** | |
| `macd_dif`, `macd_dea`, `macd` | DIF线, DEA线, MACD柱状 |
| **KDJ指标** | |
| `kdj_k`, `kdj_d`, `kdj_j` | K值, D值, J值 |
| **RSI指标** | |
| `rsi_6`, `rsi_12`, `rsi_24` | 6日/12日/24日RSI |
| **布林带** | |
| `boll_upper`, `boll_middle`, `boll_lower` | 上轨, 中轨, 下轨 |
| **CCI指标** | |
| `cci` | CCI指标值 |

## 依赖要求

需要安装以下Python包：
- baostock
- pandas
- numpy

## 注意事项

1. 首次使用时会自动登录BaoStock并加载股票列表
2. K线级别说明：
   - `d` - 日线：每个交易日一条数据
   - `w` - 周线：每周一条数据（周五收盘）
   - `m` - 月线：每月一条数据（月末收盘）
3. 复权类型说明：
   - `1` - 前复权：保持当前价格不变，调整历史价格
   - `2` - 后复权：保持历史价格不变，调整当前价格
   - `3` - 不复权：原始价格
4. 技术指标说明：
   - 均线需要足够的历史数据才能计算
   - MA120/MA250等长期均线需要至少120/250个交易日数据
   - MACD、KDJ等指标基于默认参数计算
5. 支持的指数成分股查询：
   - `000905` - 中证500指数
   - `000300` - 沪深300指数
   - `000016` - 上证50指数
6. 批量获取大量股票数据时（如500只成分股），建议分批处理或增加超时时间
7. 数据仅供参考，不构成投资建议
