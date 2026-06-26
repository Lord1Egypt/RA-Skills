# QMT配置指南

## 简介

QMT（迅投QMT极速交易终端）是目前国内散户可用的主要量化交易接口，支持A股实盘交易。本指南基于视频第2集、第6集内容整理。

---

## QMT安装

### 获取方式

1. 联系券商客户经理申请QMT账号
2. 券商会提供客户端下载链接和账号
3. 安装后登录，确保「极速交易」权限已开通

### API接口文档

- 迅投官网提供完整的API文档
- 登录后在「帮助」→「量化接口」中查看
- 参考案例：复制官网的Python示例代码

---

## QMT数据获取

### 核心API

```python
# 订阅行情
subscribe_quote(symbols)

# 获取历史数据
get_history_data(symbol, period, start_date, end_date)

# 获取账户信息
get_account_info()

# 委托下单
passorder(order_type, price_type, account, stock_code, amount, price)
```

### 数据获取示例

```python
import pandas as pd

# 参考官网示例：获取K线数据
# 1. 从QMT官网复制API示例代码
# 2. 修改股票代码和时间范围
# 3. 保存到本地CSV

# 示例：获取两只股票的因子数据
symbols = ['000001.SZ', '600000.SH']
# period: '1d', '1m', '5m', '15m'等
# start_date/end_date: 'YYYY-MM-DD'
```

---

## 因子加工

### 加工流程

1. **获取数据**：从QMT获取原始行情数据
2. **数据清洗**：处理缺失值、异常值
3. **因子计算**：使用TALib或pandas计算指标
4. **宽表整理**：合并成标准宽表格式
5. **存储**：写入QuestDB

### TALib因子计算

```python
import talib
import pandas as pd

# 假设df包含close, high, low, volume列

# MFI资金流量指标
df['mfi'] = talib.MFI(df['high'], df['low'], df['close'], df['volume'], timeperiod=14)

# RSI
df['rsi'] = talib.RSI(df['close'], timeperiod=14)

# MACD
df['macd'], df['macd_signal'], df['macd_hist'] = talib.MACD(df['close'])

# 威廉变异量
df['wvad'] = ((df['close'] - df['low']) - (df['high'] - df['close'])) / (df['high'] - df['low']) * df['volume']

# OBV能量潮
df['obv'] = talib.OBV(df['close'], df['volume'])
```

---

## 因子宽表格式

```sql
-- QuestDB中存储的宽表结构
CREATE TABLE factor_wide_table (
    symbol STRING,           -- 股票代码
    trade_date TIMESTAMP,    -- 交易日期
    obv DOUBLE,             -- 能量潮
    mfi DOUBLE,             -- 资金流量
    mom DOUBLE,             -- 动量
    rsi DOUBLE,             -- RSI
    macd DOUBLE,            -- MACD
    close DOUBLE,           -- 收盘价
    volume DOUBLE,          -- 成交量
    ret DOUBLE              -- 收益率（用于回测）
) TIMESTAMP(trade_date) PARTITION BY DAY;
```

---

## 注意事项

1. **Token保管**：QMT API Token是唯一身份凭证，切勿外泄
2. **数据频率**：日线数据足够因子研究，高频数据需额外配置
3. **数据保存**：建议定期保存数据到本地，避免重复获取
4. **股票池**：可使用行业ETF作为标的池（如视频中使用的方法）

---

## 参考命令

```bash
# QMT相关数据存放路径（建议配置到固定目录）
# Windows: D:\quant_data\
# Linux/Mac: ~/quant_data/
```
