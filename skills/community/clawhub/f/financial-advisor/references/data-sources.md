# Financial Data Sources Configuration

本文档详细说明 financial-data-analyzer skill 支持的数据源配置。

## 数据源概览

| 数据源 | 覆盖市场 | 免费/付费 | 延迟 | 推荐度 | 适用场景 |
|--------|---------|----------|------|--------|---------|
| Yahoo Finance | 全球 | 免费 | 15分钟 | ⭐⭐⭐⭐⭐ | 美股、港股、全球指数 |
| AkShare | 中国 | 免费 | 实时 | ⭐⭐⭐⭐⭐ | A股、基金、期货 |
| Tushare | 中国 | 免费+积分 | 准实时 | ⭐⭐⭐⭐ | A股专业数据 |
| 东方财富API | 中国 | 需配置 | 实时 | ⭐⭐⭐⭐ | A股实时行情 |
| Alpha Vantage | 全球 | 免费+付费 | 实时 | ⭐⭐⭐ | 美股、外汇、加密货币 |
| IEX Cloud | 美股 | 免费+付费 | 实时 | ⭐⭐⭐ | 美股实时数据 |

## 1. Yahoo Finance (yfinance)

### 特点
- **完全免费**，无需注册
- 覆盖**全球市场**（美股、港股、A股、欧洲、日本等）
- 数据质量高，历史数据完整
- Python库成熟，易于使用

### 适用场景
- 美股、港股数据采集
- 全球市场指数数据
- 长期历史数据分析
- 财务报表获取（美股）

### 使用示例

```python
import yfinance as yf

# A股示例（需要添加后缀）
stock = yf.Ticker("600519.SS")  # 贵州茅台，上交所用.SS，深交所用.SZ

# 获取历史数据
hist = stock.history(period="1y", interval="1d")

# 获取财务报表（仅美股完整支持）
income_stmt = stock.income_stmt
balance_sheet = stock.balance_sheet
cash_flow = stock.cashflow

# 获取基本信息
info = stock.info
print(info['marketCap'])  # 市值
print(info['trailingPE'])  # PE
print(info['dividendYield'])  # 股息率
```

### 股票代码格式

| 市场 | 格式 | 示例 |
|------|------|------|
| 上交所 | CODE.SS | 600519.SS (贵州茅台) |
| 深交所 | CODE.SZ | 000858.SZ (五粮液) |
| 港股 | CODE.HK | 0700.HK (腾讯) |
| 美股 | CODE | AAPL (苹果) |
| 纳斯达克 | CODE | TSLA (特斯拉) |

### 限制
- A股数据相对简单，缺少详细财务数据
- 免费版有15-20分钟延迟
- 偶尔服务不稳定，需要重试机制

---

## 2. AkShare

### 特点
- **完全免费**，专注中国金融市场
- 数据源丰富（东方财富、新浪财经、同花顺等）
- **实时数据**，无延迟
- 覆盖股票、基金、期货、期权、债券、外汇

### 适用场景
- **A股实时行情**（推荐首选）
- 详细财务报表
- 龙虎榜、大宗交易数据
- 基金净值和持仓
- 行业数据、宏观经济数据

### 使用示例

```python
import akshare as ak

# 1. 实时行情
stock_zh_a_spot_df = ak.stock_zh_a_spot_em()  # 沪深A股实时行情
print(stock_zh_a_spot_df[stock_zh_a_spot_df['代码'] == '600519'])  # 查询贵州茅台

# 2. 历史日K线
stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="600519", period="daily", start_date="20230101", end_date="20240101", adjust="qfq")

# 3. 财务报表
# 利润表
stock_financial_report_sina_df = ak.stock_financial_report_sina(stock="600519", symbol="利润表")

# 资产负债表
balance_sheet = ak.stock_financial_report_sina(stock="600519", symbol="资产负债表")

# 现金流量表
cash_flow = ak.stock_financial_report_sina(stock="600519", symbol="现金流量表")

# 4. 财务指标
stock_financial_analysis_indicator_df = ak.stock_financial_analysis_indicator(symbol="600519", start_year="2020")
# 包含：ROE、净利率、毛利率、资产负债率等

# 5. 技术指标（可选，也可自己计算）
# AkShare部分接口提供预计算指标

# 6. 基金数据
fund_open_fund_info_em_df = ak.fund_open_fund_info_em(fund="161725", indicator="单位净值走势")

# 7. 龙虎榜数据
stock_lhb_detail_daily_sina_df = ak.stock_lhb_detail_daily_sina(date="20240101")

# 8. 北向资金
stock_hsgt_north_net_flow_in_em_df = ak.stock_hsgt_north_net_flow_in_em(symbol="沪股通")

# 9. 宏观数据
macro_china_gdp_df = ak.macro_china_gdp()  # GDP数据
macro_china_cpi_df = ak.macro_china_cpi_yearly()  # CPI数据
```

### 优势
- **数据最全面**，几乎覆盖所有中国市场数据
- 实时更新，无延迟
- 完全免费，无需token

### 限制
- 仅支持中国市场
- 部分接口不稳定（依赖源网站）
- 需要处理不同接口的返回格式差异

---

## 3. Tushare

### 特点
- 专业的中国金融数据平台
- 需要**注册并获取积分**（通过分享、捐赠获取）
- 数据质量高，接口标准化
- 准实时数据（延迟5-10分钟）

### 注册与配置

1. 注册账号：https://tushare.pro/register
2. 获取Token（需要积分，免费用户有限额）
3. 配置Token：

```python
import tushare as ts

ts.set_token('YOUR_TOKEN_HERE')
pro = ts.pro_api()
```

### 使用示例

```python
import tushare as ts

pro = ts.pro_api('YOUR_TOKEN')

# 1. 日K线数据
df = pro.daily(ts_code='600519.SH', start_date='20230101', end_date='20240101')

# 2. 财务数据
# 利润表
income = pro.income(ts_code='600519.SH', start_date='20230101', end_date='20240101', fields='ts_code,ann_date,f_ann_date,end_date,revenue,operate_profit,total_profit,n_income,n_income_attr_p')

# 资产负债表
balance = pro.balancesheet(ts_code='600519.SH', start_date='20230101', end_date='20240101')

# 现金流量表
cashflow = pro.cashflow(ts_code='600519.SH', start_date='20230101', end_date='20240101')

# 3. 财务指标
fina_indicator = pro.fina_indicator(ts_code='600519.SH', start_date='20230101', end_date='20240101')

# 4. 估值数据（每日）
daily_basic = pro.daily_basic(ts_code='600519.SH', start_date='20230101', end_date='20240101', fields='ts_code,trade_date,close,pe,pb,ps,dv_ratio')

# 5. 龙虎榜
top_list = pro.top_list(trade_date='20240101')

# 6. 资金流向
moneyflow = pro.moneyflow(ts_code='600519.SH', start_date='20230101', end_date='20240101')
```

### 积分机制

| 权限 | 所需积分 | 接口频率 | 获取方式 |
|------|---------|---------|---------|
| 基础版 | 120 | 200次/分钟 | 注册(+120) |
| 中级版 | 2000 | 400次/分钟 | 捐赠、分享、贡献数据 |
| 高级版 | 5000+ | 600次/分钟 | 长期支持 |

### 优势
- 数据标准化，接口统一
- 支持复权数据
- 财务数据准确，更新及时

### 限制
- 需要积分，免费额度有限
- 历史数据需要更高积分
- 实时数据需要付费

---

## 4. 东方财富 API

### 特点
- 国内主流金融资讯平台
- 实时数据
- 需要抓包或使用第三方封装库

### 使用方式

东方财富没有官方API，但可以通过以下方式获取：

#### 方式1: 使用AkShare封装的接口

```python
import akshare as ak

# 东方财富个股实时行情
stock_individual_info_em_df = ak.stock_individual_info_em(symbol="600519")

# 东方财富资金流向
stock_individual_fund_flow_df = ak.stock_individual_fund_flow(stock="600519", market="sh")

# 东方财富财务摘要
stock_financial_abstract_df = ak.stock_financial_abstract_em(symbol="600519")
```

#### 方式2: 直接调用API（需要分析网页请求）

```python
import requests

url = "http://push2.eastmoney.com/api/qt/stock/get"
params = {
    "secid": "1.600519",  # 1.上交所 0.深交所
    "fields": "f43,f44,f45,f46,f47,f48,f50,f57,f58,f60",
    "cb": "jQuery"
}
response = requests.get(url, params=params)
```

### 优势
- 数据更新快
- 资金流向数据详细
- 个股研报、公告丰富

### 限制
- 无官方API文档
- 接口可能变动
- 需要自行解析数据格式

---

## 5. Alpha Vantage

### 特点
- 全球市场数据（美股、外汇、加密货币）
- 免费版每分钟5次请求，每天500次
- 付费版无限制

### 注册与配置

1. 注册：https://www.alphavantage.co/support/#api-key
2. 获取免费API Key

### 使用示例

```python
import requests

API_KEY = 'YOUR_API_KEY'

# 1. 日K线数据
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey={API_KEY}'
response = requests.get(url)
data = response.json()

# 2. 技术指标（SMA）
url = f'https://www.alphavantage.co/query?function=SMA&symbol=AAPL&interval=daily&time_period=20&series_type=close&apikey={API_KEY}'
response = requests.get(url)

# 3. 基本面数据
url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol=AAPL&apikey={API_KEY}'
response = requests.get(url)
```

### 优势
- 覆盖全球市场
- 技术指标预计算
- 外汇、加密货币支持

### 限制
- 免费版请求频率限制严格
- 中国市场数据有限

---

## 6. IEX Cloud

### 特点
- 美国股票市场实时数据
- 免费版每月500,000次请求
- 数据来源：美国证券交易所

### 注册与配置

1. 注册：https://iexcloud.io/
2. 获取Token

### 使用示例

```python
import requests

TOKEN = 'YOUR_TOKEN'
symbol = 'AAPL'

# 实时行情
url = f'https://cloud.iexapis.com/stable/stock/{symbol}/quote?token={TOKEN}'
response = requests.get(url)
data = response.json()

# 财务数据
url = f'https://cloud.iexapis.com/stable/stock/{symbol}/financials?token={TOKEN}'
response = requests.get(url)
```

---

## 数据源选择建议

### A股分析推荐组合

**首选方案**：AkShare + Yahoo Finance
- **AkShare**: 实时行情、财务数据、技术指标
- **Yahoo Finance**: 历史数据验证、全球对比

**专业方案**：Tushare Pro
- 需要积分，但数据最标准化

### 美股分析推荐组合

**首选方案**：Yahoo Finance
- 完全免费，数据全面

**实时交易方案**：IEX Cloud + Alpha Vantage
- 需要实时数据时使用

### 全球市场对比

**推荐方案**：Yahoo Finance
- 一个接口覆盖全球

---

## 数据质量验证

### 建议的验证流程

1. **多源对比**：关键数据从至少2个数据源获取
2. **逻辑校验**：检查数据合理性（如PE不能为负）
3. **时间对齐**：确保不同数据源时间戳一致
4. **异常处理**：处理停牌、除权除息等特殊情况

### 数据清洗检查清单

- [ ] 缺失值处理（停牌、退市）
- [ ] 异常值检测（涨跌幅超限）
- [ ] 复权处理（前复权、后复权统一）
- [ ] 时间对齐（交易日历对齐）
- [ ] 单位统一（元/万元/亿元）
- [ ] 货币统一（人民币/美元/港币）

---

## 错误处理

所有数据采集脚本应包含：

```python
import time
import logging

def fetch_with_retry(fetch_func, max_retries=3, delay=2):
    """带重试的数据获取"""
    for attempt in range(max_retries):
        try:
            return fetch_func()
        except Exception as e:
            logging.warning(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay * (attempt + 1))  # 指数退避
            else:
                raise
```

---

## 合规声明

⚠️ **重要提示**：

1. 所有数据仅用于**个人学习和研究**
2. 不得用于商业用途（除非获得授权）
3. 遵守各数据源的使用协议
4. 不得进行高频爬取影响源网站服务
5. 投资有风险，数据仅供参考

---

**配置完成后，即可在 `fetch_stock_data.py` 等脚本中使用这些数据源！**
