---
name: a-stock-data
description: "A股数据查询技能。当用户询问中国A股股价、行情、K线、财务数据、实时行情、历史数据、涨停板、选股分析时使用。支持股票代码查询（如000001、600000）、股票名称查询。"
version: 1.1.0
---

# A股数据查询技能

基于 AkShare 提供完整的 A 股数据查询能力，支持实时行情、历史K线、财务数据、技术指标分析和选股策略。

## 使用场景

✅ **自动触发，当用户说：**
- "股价"、"股票行情"、"涨停板"、"涨跌幅"
- "K线"、"历史数据"、"分时图"
- "财务数据"、"财报"、"市盈率"
- "A股"、"上证"、"深证"
- "茅台股价"、"腾讯控股"（股票名称）
- "000001"、"600000"（股票代码）
- "MACD金叉"、"RSI超卖"、"均线多头发"

## 数据源

- **AkShare**: 免费开源财经数据接口，覆盖 A股、港股、美股、基金、期货、宏观经济

## 快速命令

### 实时行情数据

#### 沪深京 A 股全部
```python
import akshare as ak

# 方式1：东方财富实时行情（推荐，更快）
stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()

# 方式2：新浪财经实时行情
stock_zh_a_spot_df = ak.stock_zh_a_spot()
```

#### 沪 A 股
```python
# 沪 A 股实时行情
stock_sh_a_spot_em_df = ak.stock_sh_a_spot_em()
```

#### 深 A
```python
# 深 A 股实时行情
stock_sz_a_spot_em_df = ak.stock_sz_a_spot_em()
```

#### 北交所
```python
# 北交所实时行情
stock_bj_a_spot_em_df = ak.stock_bj_a_spot_em()
```

#### 新股
```python
# 新股实时行情
stock_new_a_spot_em_df = ak.stock_new_a_spot_em()
```

#### 创业板
```python
# 创业板实时行情
stock_cy_a_spot_em_df = ak.stock_cy_a_spot_em()
```

#### 科创板
```python
# 科创板实时行情
stock_kc_a_spot_em_df = ak.stock_kc_a_spot_em()
```

### 历史 K线

#### 日 K线
```python
# 东方财富接口（推荐）
stock_zh_a_hist_df = ak.stock_zh_a_hist(
    symbol="000001",
    period="daily",  # daily/weekly/monthly
    start_date="20240101",
    end_date="20240331",
    adjust="qfq"     # qfq前复权/hfq后复权/""不复权
)

# 新浪财经接口
stock_zh_a_hist_df = ak.stock_zh_a_hist(
    symbol="sz000001",
    start_date="19910403",
    end_date="20210327"
)
```

#### 周 K线
```python
stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001", period="weekly")
```

#### 月 K线
```python
stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001", period="monthly")
```

### 股票信息

#### 获取所有股票代码和名称
```python
stock_info_a_code_name_df = ak.stock_info_a_code_name()
```

#### 个股详细信息
```python
# 东方财富
stock_individual_info_em_df = ak.stock_individual_info_em(symbol="茅台")

# 雪球
stock_individual_basic_info_xq_df = ak.stock_individual_basic_info_xq(symbol="SH600519")

# 雪球历史K线
stock_individual_spot_xq_df = ak.stock_individual_spot_xq(symbol="SH600519")
```

### 财务数据

#### 财务指标
```python
stock_financial_analysis_indicator_df = ak.stock_financial_analysis_indicator(
    stock="600519", 
    symbol="财务指标"
)
```

#### 资产负债表
```python
stock_balance_sheet_by_yearly_em_df = ak.stock_balance_sheet_by_yearly_em(symbol="600519")
```

#### 利润表
```python
stock_profit_sheet_by_reportly_em_df = ak.stock_profit_sheet_by_reportly_em(symbol="600519")
```

#### 现金流量表
```python
stock_cash_flow_sheet_by_reportly_em_df = ak.stock_cash_flow_sheet_by_reportly_em(symbol="600519")
```

### 市场数据

#### 指数历史
```python
# 上证指数
index_zh_a_hist_df = ak.index_zh_a_hist(
    symbol="sh000001", 
    period="daily"
)

# 深证指数
index_sz_a_hist_df = ak.index_sz_a_hist(
    symbol="sz399001", 
    period="daily"
)
```

### 资金流向与龙虎榜

#### 龙虎榜-营业部
```python
stock_individual_em_xq_df = ak.stock_individual_em_xq(symbol="SH600519")
```

#### 龙虎榜-统计
```python
# 需要东财账号
# stock_user_individual_info_em()
# stock_user_statistics_em()
```

### 板块数据

#### 强势股池
```python
stock_pool_em_df = ak.stock_pool_em()
```

#### 涨停股池
```python
stock_pool_em_df = ak.stock_pool_em()
```

### 股票市场总貌

#### 上交所
```python
stock_sse_summary_df = ak.stock_sse_summary()
```

#### 深交所
```python
# 证券类别统计
stock_szse_summary_df = ak.stock_szse_summary(date="20250619")

# 地区交易排序
stock_szse_area_summary_df = ak.stock_szse_area_summary(date="20250619")
```

## 返回格式

### 实时行情字段

|字段|说明|
|------|------|
|代码|股票代码|
|名称|股票名称|
|最新价|当前价格|
|涨跌幅|百分比|
|涨跌额|绝对值|
|成交量(手)|成交量|
|成交额|成交金额|
|昨收|昨日收盘价|
|今开|今日开盘价|
|最高|今日最高价|
|最低|今日最低价|
|振幅|波动幅度|
|换手率|换手率|
|市盈率-动态|动态市盈率|
|总市值|总市值|
|流通市值|流通市值|

### K线字段

|字段|说明|
|------|------|
|日期|交易日期|
|开盘|开盘价|
|收盘|收盘价|
|最高|最高价|
|最低|最低价|
|成交量|成交量|
|成交额|成交金额|
|振幅|振幅|
|涨跌幅|涨跌幅度|
|涨跌额|涨跌额|
|换手率|换手率|

## 技术指标分析

### 安装依赖
```bash
pip install ta-lib
```

### 常用指标

#### 均线系统（MA）
```python
import talib
import numpy as np

close = np.array(df['收盘'], dtype=float)
df['MA5'] = talib.MA(close, timeperiod=5)
df['MA10'] = talib.MA(close, timeperiod=10)
df['MA20'] = talib.MA(close, timeperiod=20)
df['MA60'] = talib.MA(close, timeperiod=60)
```

#### MACD 指标
```python
macd, signal, hist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
df['MACD'] = macd
df['MACD_SIGNAL'] = signal
df['MACD_HIST'] = hist
```

#### RSI 指标
```python
df['RSI_6'] = talib.RSI(close, timeperiod=6)
df['RSI_12'] = talib.RSI(close, timeperiod=12)
df['RSI_24'] = talib.RSI(close, timeperiod=24)
```

#### KDJ 指标
```python
high = np.array(df['最高'], dtype=float)
low = np.array(df['最低'], dtype=float)

k, d = talib.STOCH(high, low, close, fastk_period=9, slowk_period=3, slowd_period=3)
df['KDJ_K'] = k
df['KDJ_D'] = d
df['KDJ_J'] = 3 * k - 2 * d
```

#### 布林带（BOLL）
```python
upper, middle, lower = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2)
df['BOLL_UPPER'] = upper
df['BOLL_MIDDLE'] = middle
df['BOLL_LOWER'] = lower
```

#### 成交量指标
```python
volume = np.array(df['成交量'], dtype=float)

df['VOL_MA5'] = talib.MA(volume, timeperiod=5)
df['VOL_MA10'] = talib.MA(volume, timeperiod=10)

df['VOL_RATIO'] = df['成交量'] / df['VOL_MA5']
```

## 选股策略

### 策略 1：均线金叉
```python
# MA5 上穿 MA20
df['SIGNAL_MA_GOLD'] = (df['MA5'] > df['MA20']) & (df['MA5'].shift(1) <= df['MA20'].shift(1))

signals = df[df['SIGNAL_MA_GOLD'] == True]
```

### 策略 2：MACD 金叉
```python
# MACD 上穿 Signal
df['SIGNAL_MACD_GOLD'] = (df['MACD'] > df['MACD_SIGNAL']) & \
                              (df['MACD'].shift(1) <= df['MACD_SIGNAL'].shift(1))

signals = df[df['SIGNAL_MACD_GOLD'] == True]
```

### 策略 3：RSI 超卖
```python
# RSI < 30 超卖
df['SIGNAL_RSI_OVERSOLD'] = df['RSI_6'] < 30

signals = df[df['SIGNAL_RSI_OVERSOLD'] == True]
```

### 策略 4：布林带突破
```python
# 价格突破上轨
df['SIGNAL_BOLL_BREAK'] = df['收盘'] > df['BOLL_UPPER']

signals = df[df['SIGNAL_BOLL_BREAK'] == True]
```

### 策略 5：综合多因子
```python
# 多条件选股
df['SIGNAL_MULTI'] = (
    (df['MA5'] > df['MA20']) &  # 趋势向上
    (df['RSI_6'] > 50) &           # 不超卖
    (df['MACD'] > df['MACD_SIGNAL']) &  # MACD 金叉
    (df['VOL_RATIO'] > 1.5)         # 放量
)

signals = df[df['SIGNAL_MULTI'] == True]
```

## 批量选股流程

```python
import akshare as ak
import talib
import pandas as pd

# 1. 获取所有 A 股列表
stock_list = ak.stock_zh_a_spot_em()

# 2. 遍历计算指标
results = []
for index, row in stock_list.iterrows():
    code = row['代码']
    name = row['名称']
    
    # 获取历史数据
    df = ak.stock_zh_a_hist(symbol=code, period="daily")
    
    if df.empty:
        continue
    
    # 计算技术指标
    close = np.array(df['收盘'], dtype=float)
    
    # 均线
    ma5 = talib.MA(close, timeperiod=5)[-1]
    ma20 = talib.MA(close, timeperiod=20)[-1]
    
    # RSI
    rsi6 = talib.RSI(close, timeperiod=6)[-1]
    
    # MACD
    macd, signal, _ = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    macd_val = macd[-1]
    signal_val = signal[-1]
    
    # 判断选股条件（示例：均线多头 + RSI 不超卖 + MACD 金叉）
    if ma5 > ma20 and rsi6 > 50 and macd_val > signal_val:
        results.append({
            '代码': code,
            '名称': name,
            '现价': row['最新价'],
            'MA5': ma5,
            'MA20': ma20,
            'RSI': rsi6,
            'MACD': macd_val,
            '涨跌幅': row['涨跌幅']
        })

# 3. 输出结果
result_df = pd.DataFrame(results)
print(result_df.sort_values('涨跌幅', ascending=False))
```

## 涨停板查询

```python
import akshare as ak

# 获取实时行情
df = ak.stock_zh_a_spot_em()

# 筛选涨停板（涨跌幅 >= 9.9%）
df_zt = df[df['涨跌幅'] >= 9.9].sort_values('涨跌幅', ascending=False)

# 筛选跌停板（涨跌幅 <= -9.9%）
df_dt = df[df['涨跌幅'] <= -9.9].sort_values('涨跌幅', ascending=True)

print(f"涨停板数量: {len(df_zt)}")
print(f"跌停板数量: {len(df_dt)}")
print(df_zt[['代码','名称','最新价','涨跌幅','成交额']].head(20))
```

## 复权说明

股票数据复权类型：

|类型|说明|适用场景|
|------|------|----------|
|不复权（""）|原始价格|查看历史走势|
|前复权（qfq）|历史价格调整，当前价格不变|看盘、技术分析|
|后复权（hfq）|当前价格不变，历史价格调整|收益率计算|

## 股票代码规则

|市场|代码格式|示例|
|------|----------|------|
|上交所|6xxxxx|600000, 601318|
|深交所|0xxxxx|000001, 300059|
|北交所|8xxxxx|8xxxxx|

## 使用示例

### 查询个股实时行情
```python
用户：查询贵州茅台的股价
响应：使用 stock_zh_a_spot_em() 查询 600519
```

### 查询历史 K线
```python
用户：获取平安银行最近 30 天的 K线
响应：使用 stock_zh_a_hist() 查询 000001，指定日期范围
```

### 查询涨停板
```python
用户：今天有哪些股票涨停
响应：使用 stock_zh_a_spot_em() 筛选涨跌幅 >= 9.9%
```

### 查询财务数据
```python
用户：腾讯的市盈率是多少
响应：使用 stock_financial_analysis_indicator() 查询
```

### 技术分析选股
```python
用户：帮我找出 MA5 上穿 MA20 的股票
响应：计算均线指标，筛选金叉信号

用户：RSI 超卖的有哪些
响应：计算 RSI，筛选 RSI < 30

用户：MACD 金叉且放量的股票
响应：计算 MACD 和成交量，综合筛选

用户：多因子选股：趋势向上 + MACD 金叉 + RSI>50
响应：多条件综合筛选
```

## 错误处理

常见错误及处理：

|错误类型|可能原因|解决方法|
|------|----------|----------|
|KeyError|股票代码不存在或输入错误|检查代码并重试|
|TimeoutError|网络超时|重试或检查连接|
|EmptyDataError|当天无数据（非交易日）|确认是否交易日|

## 注意事项

1. **频率限制**: 避免频繁请求，建议缓存结果
2. **数据延迟**: 实时数据可能有 1-5 分钟延迟
3. **复权处理**: 查询历史数据时注意复权方式选择
4. **代码规范**: 6 位数字代码，补齐前导 0（如 1 → 000001）

## 支持的数据范围

- ✅ A 股实时行情（沪深京、沪深北、沪深深）
- ✅ B 股实时行情
- ✅ 港股实时行情
- ✅ 美股实时行情
- ✅ 创业板、科创板、新股
- ✅ 历史 K线数据（日、周、月）
- ✅ 财务数据（资产负债表、利润表、现金流量表）
- ✅ 技术指标分析（MA、MACD、RSI、KDJ、BOLL）
- ✅ 龙虎榜、资金流向
- ✅ 板块数据、概念股
- ✅ 指数数据
- ✅ 市场总貌统计

---
