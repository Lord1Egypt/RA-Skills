# 数据源优先级与字段映射

## 数据源优先级

按照 AGENTS.md 中的金融数据规则，数据获取优先级为：

```
iFinD → Tushare → AkShare → Alpha Vantage
```

### 各数据源特性

| 数据源 | 覆盖范围 | 优势 | 授权要求 |
|--------|----------|------|----------|
| **iFinD** | A股/港股/基金/宏观/新闻 | 语义化查询，最全面 | API Token |
| **Tushare** | A股/港股/期货/宏观 | 标准化API，免费层 | TUSHARE_TOKEN |
| **AkShare** | A股/期货/外汇 | 免费，实时数据 | 无 |
| **Alpha Vantage** | 美股/外汇/大宗 | 国际市场 | API Key |

## 字段映射表

### 1. 公司基本信息

| 字段 | iFinD 查询 | Tushare API | AkShare |
|------|------------|-------------|---------|
| 公司名称 | `{股票} 公司名称` | `stock_company.name` | `stock_individual_info_em` |
| 股票代码 | `{股票} 代码` | `ts_code` | `代码` |
| 上市交易所 | `{股票} 交易所` | `exchange` | AkShare 不提供 |
| 申万行业 | `{股票} 申万行业` | `company_classify` | `行业` |

### 2. 市场信息

| 字段 | Tushare API | AkShare |
|------|-------------|---------|
| 最新股价 | `daily.close` | `stock_zh_a_spot_em['最新价']` |
| 价格日期 | `daily.trade_date` | AkShare 实时 |
| 52周最高 | `daily.high` (近365天) | `stock_zh_a_spot_em['最高']` |
| 52周最低 | `daily.low` (近365天) | `stock_zh_a_spot_em['最低']` |
| PE(TTM) | `daily_basic.pe_ttm` | AkShare 不提供 |
| 预测PE | 需 iFinD | 不提供 |
| 总市值 | `daily_basic.total_mv` | `stock_zh_a_spot_em['总市值']` |
| 股息率 | `daily_basic.dividend_yield` | AkShare 不提供 |

### 3. 财务数据（近10年）

| 字段 | Tushare API | 说明 |
|------|-------------|------|
| 每股营收 | `income.revenue / balancesheet.total_shares` | 计算得出 |
| 每股现金流 | `cashflow.n_cash_flows_oper_act_per_share` | 直接获取 |
| 每股盈利 | `eps.eps` | 直接获取 |
| 每股派息 | `dividend.dividend` | 直接获取 |
| 每股净资产 | `balancesheet.total_hldr_eqy_exc_min_int / total_shares` | 计算得出 |
| 年度平均PE | 需计算每日PE的平均值 | 自算 |
| 年度派息率 | `dividend.dividend / eps.eps` | 计算得出 |
| 主营收入 | `income.revenue` | 亿元 |
| 毛利率 | `(income.revenue - income.oper_cost) / income.revenue` | 计算得出 |
| 营业利润率 | `income.oper_profit / income.revenue` | 计算得出 |
| 库存 | `balancesheet.inventory` | 亿元 |
| 净利润 | `income.net_profit` | 亿元 |
| 净利润率 | `income.net_profit / income.revenue` | 计算得出 |

### 4. 股东信息

| 字段 | Tushare API |
|------|-------------|
| 控股股东 | `top10_holders[0].holder_name` |
| 前五大股东 | `top10_holders[:5]` |
| 持股比例 | `top10_holders.hold_ratio` |

### 5. K线数据

| 字段 | Tushare API |
|------|-------------|
| 日期 | `monthly.trade_date` |
| 开盘价 | `monthly.open` |
| 最高价 | `monthly.high` |
| 最低价 | `monthly.low` |
| 收盘价 | `monthly.close` |
| 成交额 | `monthly.amount` |

### 6. 新闻数据

| 数据源 | 方式 |
|--------|------|
| iFinD | 语义查询 `{股票} 近30天重要新闻` |
| AkShare | `stock_news_em` |

## API 调用示例

### Tushare 获取实时数据

```python
import tushare as ts
ts.set_token(os.environ['TUSHARE_TOKEN'])
pro = ts.pro_api()

# 获取日线数据
daily = pro.daily(ts_code='000001.SZ', start_date='20250101')

# 获取估值指标
basic = pro.daily_basic(ts_code='000001.SZ', fields='pe_ttm,total_mv')

# 获取财务数据
income = pro.income(ts_code='000001.SZ', start_period='202001')
```

### AkShare 获取实时数据

```python
import akshare as ak

# 实时行情
realtime = ak.stock_zh_a_spot_em()

# 个股信息
info = ak.stock_individual_info_em(symbol='000001')

# 新闻
news = ak.stock_news_em(symbol='000001')
```

## 股票代码格式

| 市场 | 格式示例 |
|------|----------|
| 上交所 | `600519.SH` |
| 深交所 | `000001.SZ` |
| 北交所 | `430047.BJ` |

AkShare 使用不带后缀的格式（如 `000001`）。