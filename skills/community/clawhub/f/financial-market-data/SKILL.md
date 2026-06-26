# Financial Market Data Skill

_统一金融行情数据接口 — 多源互补、自动降级、永不单点故障_

---

## 安装指南（全新 OpenClaw 实例）

### 第一步：复制 Skill 目录

将整个 `skills/financial-market-data/` 目录复制到目标机器的对应位置：

```
~/.openclaw/workspace/skills/financial-market-data/
```

目录结构：
```
financial-market-data/
├── SKILL.md              # 本文件
├── skill.yaml            # Skill 元数据
└── python/
    ├── pyproject.toml   # Python 依赖
    ├── template.py       # 基础接口（TickFlow/pytdx/baostock/akshare）
    └── ths.py             # 同花顺专用接口（新增）
```

### 第二步：安装 Python 依赖（推荐 uv）

```bash
cd ~/.openclaw/workspace
uv sync
```

或使用 pip：

```bash
pip install tickflow akshare baostock pytdx requests pandas
```

### 第三步：使用说明

在任意 Python 脚本中引用：

```python
import sys
sys.path.insert(0, 'skills/financial-market-data/python')
from ths import get_daily_k, get_1min_k, get_intraday, get_realtime
from template import get_daily_k as tk_daily, get_realtime_eastmoney
```

---

## 一、同花顺数据接口 ✅ 推荐（无需注册，完全免费）

同花顺官方免费接口，**1分钟K线最强**（约821条历史，覆盖2009年至今）。

### 1.1 同花顺 日K线

```python
import sys
sys.path.insert(0, 'skills/financial-market-data/python')
from ths import get_daily_k, get_daily_k_page

# 获取日K（每次最多140条，总量约3856条）
records = get_daily_k("300006")  # 莱美药业
for r in records[-5:]:
    print(r['date'], r['close'], r['volume'])

# 翻页获取更早数据（以第一条记录日期为end参数）
older = get_daily_k_page("300006", end_date="20250902")
```

### 1.2 同花顺 1分钟K线（最强免费源）

```python
from ths import get_1min_k

# 获取1分钟K（全部历史，约821条）
records = get_1min_k("300006")
print(f"共 {len(records)} 条, {records[0]['date']} ~ {records[-1]['date']}")
```

**优势对比：**

| 数据源 | 1分钟K条数 | 免费 | 注册 |
|--------|-----------|------|------|
| **同花顺** | **约821条** | ✅ | 不需要 |
| pytdx | 有限制 | ✅ | 不需要 |
| BaoStock | 有限制 | ✅ | 不需要 |
| 东方财富Level2 | 完整 | ❌ | 需要付费 |

### 1.3 同花顺 分时数据

```python
from ths import get_intraday

# 获取分时（每分钟汇总，需差分计算增量）
result = get_intraday("300006")
for r in result['records'][-10:]:
    print(r['time'], r['price'], r['volume'], '手/分钟')
```

### 1.4 同花顺 实时行情

```python
from ths import get_realtime, get_multi_realtime

# 单只
rt = get_realtime("300006")
print(rt['price'])

# 批量
data = get_multi_realtime(["300006", "002560", "601975"])
for d in data:
    print(d.get('code'), d.get('price'))
```

### 1.5 同花顺接口字段说明

| 周期 | URL路径 | 返回条数 | 数据格式 |
|------|---------|---------|---------|
| 日K | `/v6/line/hs_{code}/01/his.js` | 140条/次，总3856条 | 日期,开,高,低,收,量,额,换手 |
| **1分钟K** | `/v6/line/hs_{code}/11/last.js` | **全部约821条** | 同上 |
| 60分钟K | `/v6/line/hs_{code}/60/last.js` | 140条/次 | 日期时间(YYYYMMDDHHMM),开,高,低,收,量,额,换手 |
| 分时 | `/v6/line/hs_{code}/01/last.js` | 约140条/日 | 累计量，需差分算增量 |
| 实时 | `/v6/realtime/hs_{code}.js` | 1条即时 | 价格/高/低/量/额/五档 |

> **注意：** 同花顺接口返回JSONP格式（`quotebridge_v6_line_hs_xxx({"num":...})`），需解析JSONP并用分号分割数据字段。

---

## 二、A股日K线

### 2.1 TickFlow（推荐，接口简洁）

```python
from tickflow import TickFlow
tf = TickFlow.free()
df = tf.klines.get("600519.SH", period="1d", count=100, as_dataframe=True)
# 返回字段：trade_date, open, high, low, close, volume
```

### 2.2 BaoStock（全量历史，支持复权）

```python
import baostock as bs
bs.login()
rs = bs.query_history_k_data_plus(
    "sz.000001",
    "date,code,open,high,low,close,volume,pctChg",
    start_date="20200101",
    end_date="20260404",
    frequency="d",
    adjustflag="3"
)
data_list = []
while rs.next:
    data_list.append(rs.get_row_data())
bs.logout()
```

---

## 三、A股分钟K线

### 3.1 pytdx 通达信接口（1分钟K）

```python
from pytdx.hq import TdxHq_API
api = TdxHq_API()
if api.connect('218.75.126.9', 7709):
    data = api.get_security_bars(9, 0, "000001", 0, 100)  # category=9=1分钟K
    api.disconnect()
```

### 3.2 BaoStock（5/15/30/60分钟）

```python
rs = bs.query_history_k_data_plus(
    "sz.000001",
    "date,time,code,open,high,low,close,volume",
    start_date="20260401",
    end_date="20260404",
    frequency="5",  # 5=5分钟
    adjustflag="3"
)
```

---

## 四、港股/美股

### 4.1 港股日K

```python
# TickFlow（推荐）
df = tf.klines.get("00700.HK", period="1d", count=100)

# AkShare（备选）
import akshare as ak
df = ak.stock_hk_daily(symbol="00700", start_date="20240101", end_date="20260404", adjust="qfq")
```

### 4.2 美股日K

```python
# TickFlow（推荐）
df = tf.klines.get("AAPL.US", period="1d", count=100)

# AkShare（备选）
df = ak.stock_us_daily(symbol="AAPL", start_date="20240101", end_date="20260404", adjust="qfq")
```

### 4.3 港股/美股实时

```python
# 港股实时
df = ak.stock_hk_spot_em()
# 美股实时
df = ak.stock_us_spot_em()
```

---

## 五、期货/期权

### 5.1 期货日K（AkShare）

```python
import akshare as ak
df = ak.futures_zh_daily(symbol="au2504", start_date="20240101", end_date="20260404")
```

### 5.2 期货分钟K（pytdx）

```python
# 上海期货（market=47）
data = api.get_security_bars(9, 47, "au2504", 0, 100)
# 大连/郑州（market=1）
data = api.get_security_bars(9, 1, "i2505", 0, 100)
```

---

## 六、ETF/基金

```python
import akshare as ak

# 沪深300ETF日K
df = ak.fund_etf_hist_sina(symbol="sh510300")

# ETF实时行情
df = ak.fund_etf_spot_em()

# 场外基金净值
df = ak.fund_open_fund_info_em(symbol="000001", indicator="累计净值走势")
```

---

## 七、实时行情

### 7.1 东方财富MX API（需要Token）

```python
import requests, json

api_key = "替换为你自己的MX API Key，申请地址：https://openapi.eastmoney.com/mx/v1/api-docs"
url = "https://mkapi2.dfcfs.com/finskillshub/api/claw/query"

payload = {
    "toolQuery": json.dumps({
        "func": "get_quote_list_ts",
        "params": ["600519.SH,000001.SZ", 1]
    })
}
headers = {"Content-Type": "application/json", "apiKey": api_key}
resp = requests.post(url, json=payload, headers=headers, timeout=15)
data = resp.json()
```

### 7.2 东方财富 Direct（无需Token，部分接口）

```python
import requests
url = "https://push2.eastmoney.com/api/qt/stock/get"
params = {
    "secid": "1.600519",
    "fields": "f43,f44,f45,f46,f47,f48,f50,f57,f58,f107,f169,f170",
}
r = requests.get(url, params=params, timeout=10)
# f43=最新价 f170=涨跌幅 f57=代码 f58=名称
```

---

## 八、板块/行业

```python
import akshare as ak

# 行业板块列表
df = ak.stock_board_industry_name_em()

# 概念板块列表
df = ak.stock_board_concept_name_em()

# 板块内个股
df = ak.stock_board_industry_cons_em(symbol="半导体")

# 行业涨幅榜
df = ak.stock_board_industry_rank_em()
```

---

## 九、财务数据

```python
import baostock as bs
bs.login()

# 盈利能力
rs = bs.query_profit_data(code="sz.000001", year=2024, quarter=4)
df = rs.get_data()

# 成长能力
rs = bs.query_growth_data(code="sz.000001", year=2024, quarter=4)

# 杜邦分析
rs = bs.query_dupont_data(code="sz.000001", year=2024, quarter=4)

bs.logout()
```

---

## 十、资金流向

```python
import akshare as ak

# 个股资金流向
df = ak.stock_individual_fund_flow(stock="000001", market="sh")

# 大单净流入
df = ak.stock_individual_fund_flow(stock="000001", market="sh", symbol="大单净流入")
```

---

## 十一、宏观数据

```python
import akshare as ak
df = ak.macro_china_gdp()           # GDP
df = ak.macro_china_cpi()            # CPI
df = ak.macro_china_money_supply()  # 货币供应量
```

---

## 十二、推荐组合方案

| 方案 | 适用场景 | 日K | 1分钟K | 实时行情 | 板块/财务 |
|:---:|---|:---:|:---:|:---:|:---:|
| **A** | 纯免费无需注册 | TickFlow | **同花顺821条** | AkShare Direct | AkShare |
| **B** | 最佳体验（需Key） | TickFlow | **同花顺** | **东方财富MX API** | AkShare + BaoStock |
| **C** | A股专注 | BaoStock | BaoStock | AkShare Direct | BaoStock + AkShare |

---

## 十三、已知问题 & 解决方案

| 问题 | 解决方案 |
|---|---|
| **同花顺1分钟K最强** | ✅ 约821条，2009年至今，完全免费 |
| TickFlow免费版无分钟K | → 改用同花顺1分钟K 或 pytdx |
| BaoStock分钟K日期格式报错 | → 用 `frequency="5"` 而非 `"1min"` |
| AkShare网络不稳定 | → 添加重试机制，或切换到同花顺 |
| 东方财富MX API中文乱码 | → 数值正常，字段名用正则匹配数字ID绕过 |
| pytdx连接失败（防火墙/封禁） | → 换用 同花顺1分钟K |
| 东财push2his(K线)被拒 | → 换用 同花顺日K |
| 英为财情（Cloudflare） | → 完全无法突破，需付费API |

---

## 十四、Token 速查表

| 接口 | Key | 状态 |
|---|---|:---:|
| 东方财富 MX API | `替换为你自己的MX API Key，申请地址：https://openapi.eastmoney.com/mx/v1/api-docs` | ✅ 已配置 |

> **注意：** 同花顺、TickFlow、BaoStock、AkShare、pytdx 均为免费无需注册接口，**同花顺1分钟K是免费接口中最强的**。
