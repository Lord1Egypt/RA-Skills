# Stock Technical Analysis

股票技术分析工具 - 基于东方财富数据

## 功能

- K线数据获取（日/周/月）
- 技术指标计算：KDJ、MACD、BOLL、MA
- 综合交易信号分析
- 资金流向排名

## 安装

```bash
pip install -r requirements.txt
```

## 使用

```python
from eastmoney_spider import EastmoneySpider
from indicators import calculate_kdj, calculate_macd, calculate_boll, get_latest_signals

spider = EastmoneySpider()

# 获取K线数据
df = spider.get_stock_kline("600519", days=100)

# 计算技术指标
kdj = calculate_kdj(df)
macd = calculate_macd(df)
boll = calculate_boll(df)
signals = get_latest_signals(df)

print(f"股票: {df.iloc[0]['name']}")
print(f"收盘价: {df.iloc[-1]['close']}")
print(f"KDJ信号: {signals['kdj']['status']}")
```

## 依赖

- requests >= 2.28.0
- pandas >= 1.5.0
- numpy >= 1.21.0

## 许可证

MIT