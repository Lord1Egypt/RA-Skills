# Tushare API 常用接口

## 通用说明

- 所有接口需要初始化：
```python
import tushare as ts
pro = ts.pro_api(your_token)
```

## A股港股基础信息

### 股票列表
```python
# A股
data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

# 港股
data = pro.hk_basic()
```

## 日线行情
```python
# A股
df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)

# 港股
df = pro.hk_daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
```

## 财务指标
```python
# A股
df = pro.fina_indicator(ts_code=ts_code)

# 港股也可以通过此接口获取
```

## 每日指标（包含技术指标基础数据）
```python
df = pro.daily_basic(ts_code=ts_code, trade_date=trade_date)
```

## 代码转换规则

Tushare格式：`[代码].[交易所后缀]`
- 沪市A股：`XXXXXX.SH`
- 深市A股：`XXXXXX.SZ`
- 北交所A股：`XXXXXX.BJ`
- 港股：`XXXXXX.HK`

用户输入6位A股代码自动补全后缀，5位港股代码自动补全 `.HK`
