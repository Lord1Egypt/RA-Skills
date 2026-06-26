---
name: china-stock-quotes
description: Query real-time A-share stock prices, major indices, and sector data across Shanghai, Shenzhen, and Beijing exchanges. Includes individual stocks, market indices, board indices, and industry sector performance.
emoji: 📈
metadata:
  openclaw:
    requires:
      bins:
        - curl
---

# China Stock Quotes — A股实时行情查询

Real-time stock prices for Shanghai (SSE), Shenzhen (SZSE), and Beijing (BSE) exchanges. Covers individual stocks, major indices, and industry sector data.

## Exchange & Stock Code Reference

### Stock Prefixes

| Exchange | Prefix | Examples | Description |
|:---------|:-------|:---------|:------------|
| 上证所 SSE | `sh` | sh600519(茅台), sh600036(招行) | 主板A股 600/601/603 |
| 上证所 SSE | `sh` | sh688981(中芯) | 科创板 688 |
| 深交所 SZSE | `sz` | sz000858(五粮液), sz000001(平安) | 主板A股 000/001 |
| 深交所 SZSE | `sz` | sz002415(海康) | 中小板 002 |
| 深交所 SZSE | `sz` | sz300750(宁德), sz300059(东方) | 创业板 300 |
| 深交所 SZSE | `sz` | sz301025 | 创业板注册制 301 |
| 北交所 BSE | `bj` | bj835185(贝特瑞) | 北交所 8xxxxx |

### Major Indices

| Index | Code | Description |
|:------|:-----|:------------|
| 上证指数 | `s_sh000001` | 上证综合指数 |
| 深证成指 | `s_sz399001` | 深证成份指数 |
| 创业板指 | `s_sz399006` | 创业板指数 |
| 科创50 | `s_sh000688` | 科创板50指数 |
| 沪深300 | `s_sh000300` | 沪深300指数 |
| 上证50 | `s_sh000016` | 上证50指数 |
| 中证500 | `s_sh000905` | 中证500指数 |
| 中证1000 | `s_sh000852` | 中证1000指数 |
| 创业板50 | `s_sz399673` | 创业板50指数 |
| 北证50 | `s_bj899050` | 北证50指数 |

### Key Individual Stocks

| Stock | Code | Sector |
|:------|:-----|:-------|
| 贵州茅台 | sh600519 | 白酒/消费 |
| 宁德时代 | sz300750 | 新能源/电池 |
| 招商银行 | sh600036 | 银行/金融 |
| 五粮液 | sz000858 | 白酒/消费 |
| 中国平安 | sh601318 | 保险/金融 |
| 东方财富 | sz300059 | 券商/金融科技 |
| 紫金矿业 | sh601899 | 有色金属 |
| 中信证券 | sh600030 | 券商/金融 |
| 比亚迪 | sz002594 | 新能源汽车 |
| 药明康德 | sh603259 | 医药/CRO |

## How to Use

### Step 1: Identify the stock code

Format: `<prefix><code>` (e.g., `sh600519` = 贵州茅台)

**Common stock codes:**
- 贵州茅台: sh600519
- 宁德时代: sz300750
- 招商银行: sh600036
- 五粮液: sz000858
- 沪深300指数: s_sh000300
- 上证指数: s_sh000001

### Step 2: Fetch data

**Method A: Browser Snapshot (full real-time data)**
1. Navigate to `https://finance.sina.com.cn/realstock/company/<CODE>/nc.shtml`
2. Wait ~2s for page to fully render (trading hours only; non-trading hours shows last close)
3. Take a snapshot (compact mode)
4. Extract: 最新价(price), 涨跌幅(change%), 今开(open), 最高(high), 最低(low), 成交量(volume)

**Example: 贵州茅台**
```
Navigate → https://finance.sina.com.cn/realstock/company/sh600519/nc.shtml
Snapshot → look for price data
```

**Method B: curl (Quick — for stocks)**
```bash
curl -s -e "https://finance.sina.com.cn" "https://hq.sinajs.cn/list=sh600519,sz300750,sh600036"
```

Response format for stocks (comma-separated):
```
var hq_str_sh600519="name,open,prev_close,current,high,low,bid,ask,volume,amount,..."
```

**Key field indices:**
| Index | Field | Description |
|:-----:|:------|:------------|
| 0 | name | 股票名称 |
| 1 | open | 今开 |
| 2 | prev_close | 昨收 |
| 3 | current | 最新价 |
| 4 | high | 最高 |
| 5 | low | 最低 |
| 8 | volume | 成交量(手) |
| 9 | amount | 成交额(元) |

**Method C: curl (Quick — for indices)**
```bash
curl -s -e "https://finance.sina.com.cn" "https://hq.sinajs.cn/list=s_sh000001,s_sz399001,s_sz399006,s_sh000300,s_sh000016"
```

Response format for indices:
```
var hq_str_s_sh000001="name,current,change,change%,volume,amount"
```

### Step 3: Calculate change

**For stocks:**
```
涨跌额 = current - prev_close
涨跌幅 = (current - prev_close) / prev_close * 100
```

**For indices:**
```
涨跌额 = change (field index 2)
涨跌幅 = change% (field index 3)
```

### Step 4: Format output

**Single stock:**
```
📈 [名称] 实时行情 (时间)
当前: ¥XXX.XX  涨跌: +X.XX (+X.XX%) 🟢
开盘: ¥XXX.XX  最高: ¥XXX.XX
最低: ¥XXX.XX  昨收: ¥XXX.XX
成交量: XXX手  成交额: XXX亿
```

**Multiple stocks (compact table):**
```
📈 A股组合行情 (时间)
名称      代码      最新价    涨跌幅
贵州茅台  sh600519  XXX.XX  +X.XX% 🟢
宁德时代  sz300750  XXX.XX  -X.XX% 🔴
招商银行  sh600036  XXX.XX  +X.XX% 🟢
```

**Major indices:**
```
📊 A股大盘指数
上证指数  XXXX.XX  -X.XX (-X.XX%) 🔴
深证成指  XXXX.XX  +X.XX (+X.XX%) 🟢
创业板指  XXXX.XX  +X.XX (+X.XX%) 🟢
科创50    XXXX.XX  +X.XX (+X.XX%) 🟢
```

## Trading Hours

| Session | Time (GMT+8) |
|:--------|:-------------|
| Morning | 09:30-11:30 |
| Afternoon | 13:00-15:00 |
| 集合竞价(开盘) | 09:15-09:25 |

Note: A-shares have NO night session. No trading on weekends or public holidays.

## Common Batch Queries

**Top 10 liquid stocks:**
```bash
curl -s -e "https://finance.sina.com.cn" "https://hq.sinajs.cn/list=sh600519,sz300750,sh600036,sz000858,sh601318,sz300059,sh601899,sh600030,sz002594,sh603259"
```

**Major indices snapshot:**
```bash
curl -s -e "https://finance.sina.com.cn" "https://hq.sinajs.cn/list=s_sh000001,s_sz399001,s_sz399006,s_sh000688,s_sh000300,s_sh000016,s_sz399673"
```

## Special Notes

- A-shares have **price limits**: 主板 ±10%, 科创板/创业板 ±20%, 北交所 ±30%
- The Sina API requires a proper `Referer` header (`https://finance.sina.com.cn`) when called via direct curl
- Non-trading hours: data reflects the last trading day's close
- Index code prefix `s_sh` for Shanghai indices, `s_sz` for Shenzhen indices
- Stock data API response is GBK-encoded; use `iconv` or `curl` with charset handling for Chinese names
- Volume in **手** (1手 = 100 shares), Amount in **元**
