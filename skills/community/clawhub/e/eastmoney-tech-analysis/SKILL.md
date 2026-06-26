# 股票技术分析 Skill (Stock Technical Analysis)

## 技能信息
- **名称**: stock-technical-analysis
- **描述**: 股票技术分析工具 - 获取K线数据、计算技术指标（KDJ/MACD/BOLL/MA）、资金流向排名
- **触发关键词**: 股票分析、技术指标、查股票、行情分析、KDJ、MACD、BOLL

## 功能
1. **K线数据获取** - 获取股票历史行情数据（日/周/月K线）
2. **技术指标计算** - KDJ、MACD、BOLL、MA 均线
3. **资金流向** - 主力资金排名（今日/5日/10日）
4. **综合信号** - 金叉/死叉、超买/超卖状态

## 环境依赖
- Python 3.8+
- requests>=2.28.0
- pandas>=1.5.0
- numpy>=1.21.0

## 使用示例

### 1. 完整分析一只股票
```python
from eastmoney_spider import EastmoneySpider
from indicators import (
    calculate_kdj, 
    calculate_macd, 
    calculate_boll, 
    calculate_ma,
    get_latest_signals
)

spider = EastmoneySpider()

# 获取K线数据（默认100天）
df = spider.get_stock_kline("600519", days=100)

# 计算各技术指标
kdj = calculate_kdj(df)
macd = calculate_macd(df)
boll = calculate_boll(df)
ma = calculate_ma(df)
signals = get_latest_signals(df)

# 输出结果
print(f"股票: {df.iloc[0]['name']}")
print(f"收盘价: {df.iloc[-1]['close']}")
print(f"KDJ: K={kdj['k'][-1]:.1f} D={kdj['d'][-1]:.1f} J={kdj['j'][-1]:.1f}")
print(f"MACD: DIF={macd['dif'][-1]:.3f} DEA={macd['dea'][-1]:.3f}")
print(f"BOLL: 上轨={boll['upper'][-1]:.2f} 中轨={boll['middle'][-1]:.2f} 下轨={boll['lower'][-1]:.2f}")
print(f"综合信号: {signals}")
```

### 2. 获取资金流向排名
```python
from eastmoney_spider import EastmoneySpider

spider = EastmoneySpider()

# 今日主力资金排名
date, df = spider.fetch_capital_flow_rank(days=0, limit=20)

# 5日主力资金排名
date, df = spider.fetch_capital_flow_rank(days=5, limit=20)

print(df.head(10))
```

### 3. 命令行直接运行
```bash
python stock_analyze.py 600519
python stock_analyze.py 000001 --json
```

## 指标说明

### KDJ 随机指标
- **K值**: 快速随机指标
- **D值**: 慢速随机指标  
- **J值**: 3×K - 2×D
- **信号**: K/D金叉(买)、K/D死叉(卖)
- **超买**: J>80 | **超卖**: J<20

### MACD 指数平滑异同移动平均线
- **DIF**: 快线 (EMA12 - EMA26)
- **DEA**: 慢线 (DIF的EMA9)
- **MACD**: (DIF-DEA)×2
- **信号**: DIF上穿DEA(金叉)、下穿DEA(死叉)
- **趋势**: DIF>DEA 多头 | DIF<DEA 空头

### BOLL 布林线
- **上轨**: 中轨 + 2×标准差
- **中轨**: 20日均线
- **下轨**: 中轨 - 2×标准差
- **信号**: 突破上轨(超买)、跌破下轨(超卖)

### MA 移动平均线
- **MA5**: 5日均线（短期）
- **MA10**: 10日均线（短期）
- **MA20**: 20日均线（中期）
- **MA60**: 60日均线（长期）

## 返回格式

### 综合信号 (get_latest_signals)
```python
{
    'kdj': {
        'signal': 1,  # 1=金叉, -1=死叉, 0=无
        'status': '超买/超卖/正常',
        'j': 85.5    # J值
    },
    'macd': {
        'signal': 0,
        'trend': '多头/空头'
    },
    'boll': '突破上轨/跌破下轨/震荡区间',
    'price': {
        'close': 1460.0,
        'pct_chg': 0.12
    },
    'date': '2026-04-03'
}
```

## 注意事项
- 股票代码需要是6位数字（如600519、000001）
- 默认获取100天日K线数据
- 资金流向API返回可能包含期货/债券数据
- 本技能仅供技术分析参考，不构成投资建议