# 回测方法

## 简介

回测是验证量化策略有效性的核心步骤。本指南基于视频第3集内容整理，介绍使用Backtrader进行因子回测的方法。

---

## 核心指标

### IC（信息系数）

**定义**：因子排序与未来收益排序的相关性（Spearman相关系数）

**解读**：
- IC > 0：正相关
- IC < 0：负相关（符号反转后可用）
- |IC|越大，预测能力越强

### IR（信息比率）

**公式**：IR = Mean(IC) / Std(IC)

**解读**：
- IR > 0.5：因子较稳定
- IR > 1：因子非常稳定
- IR < 0.3：因子不稳定

### T值

**公式**：T = Mean(IC) / (Std(IC) / sqrt(n))

**显著性**：
- |T| > 1.96：p < 0.05，显著
- |T| > 2.58：p < 0.01，极显著

---

## Backtrader回测框架

### 安装

```bash
uv pip install backtrader
```

### 基础结构

```python
import backtrader as bt
import pandas as pd

class FactorBacktest(bt.Strategy):
    """基于因子的选股策略"""
    
    def __init__(self):
        self.order = None
        self.rebalance_day = 0
        self.hold_days = 5  # 调仓周期
        self.top_n = 20     # 选股数量
    
    def next(self):
        # 每隔hold_days天调仓
        if len(self) % self.hold_days != 0:
            return
        
        # 获取当前日期的因子数据
        date = self.datas[0].datetime.date(0)
        
        # 选取因子排名前N的标的
        selected = self.select_stocks(date, self.top_n)
        
        # 调仓
        self.rebalance(selected)
    
    def select_stocks(self, date, top_n):
        """根据因子选择股票"""
        # 筛选因子值最高的前N只
        return selected
    
    def rebalance(self, selected):
        """执行调仓"""
        # 卖出不在selected中的持仓
        # 买入selected中未持仓的
        pass
```

---

## 完整回测示例

### 数据准备

```python
import pandas as pd
import backtrader as bt

# 从QuestDB加载因子数据
def load_factor_data():
    # 连接QuestDB查询
    query = """
        SELECT symbol, trade_date, mfi, rsi, mom, close, volume
        FROM factor_wide_table
        WHERE trade_date >= '2025-01-01'
    """
    df = pd.read_sql(query, engine)
    df['trade_date'] = pd.to_datetime(df['trade_date'])
    return df

# 准备回测数据
data = load_factor_data()
```

### 因子选股逻辑

```python
class MultiFactorStrategy(bt.Strategy):
    params = (
        ('hold_days', 5),
        ('top_n', 20),
        ('weights', None),
    )
    
    def __init__(self):
        self.order = None
        self.factor_data = None
        
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                pass
            elif order.issell():
                pass
        self.order = None
    
    def next(self):
        # 非调仓日不操作
        if len(self) % self.params.hold_days != 0:
            return
        
        # 获取当日因子值
        date = self.datas[0].datetime.date(0)
        
        # 选取前N只
        selected = self.get_top_stocks(date, self.params.top_n)
        
        # 执行调仓
        self.rebalance_portfolio(selected)
    
    def get_top_stocks(self, date, top_n):
        """获取因子排名前N的股票"""
        # 实际应用中需关联因子数据
        return selected[:top_n]
    
    def rebalance_portfolio(self, selected):
        """调仓逻辑"""
        # 计算目标权重
        weight = 1.0 / len(selected) if selected else 0
        
        for d in self.datas:
            if d.code in selected:
                # 买入
                target_size = int(self.broker.getvalue() * weight / d.close)
                self.buy(data=d, size=target_size)
            else:
                # 卖出
                if self.getposition(d).size > 0:
                    self.close(data=d)
```

### 运行回测

```python
cerebro = bt.Cerebro()

# 添加数据
for symbol in symbols:
    data_feed = bt.feeds.PandasData(
        dataname=df[df['symbol'] == symbol],
        datetime='trade_date',
        open='open',
        high='high',
        low='low',
        close='close',
        volume='volume',
        openinterest=-1
    )
    cerebro.adddata(data_feed)

# 设置初始资金
cerebro.broker.setcash(1000000.0)

# 设置手续费
cerebro.broker.setcommission(commission=0.001)

# 添加策略
cerebro.addstrategy(MultiFactorStrategy)

# 运行回测
print(f'初始资金: {cerebro.broker.getvalue():.2f}')
results = cerebro.run()
print(f'最终资金: {cerebro.broker.getvalue():.2f}')
```

---

## 关键注意事项

### 1. 避免未来函数

```python
# ❌ 错误：用当天因子值计算当天收益
today_factor = get_factor(date)
today_return = get_return(date)

# ✅ 正确：用前一天因子值选股，用当天收益计算
yesterday_factor = get_factor(date - 1)
today_return = get_return(date)
```

### 2. T+1交易

- 收盘后计算因子值
- 次日开盘价执行交易
- 考虑滑点和手续费

### 3. 参数优化

```python
# 测试不同参数组合
for hold_days in [3, 5, 10, 20]:
    for top_n in [10, 20, 30, 50]:
        cerebro.addstrategy(MultiFactorStrategy, 
                          hold_days=hold_days,
                          top_n=top_n)
```

---

## 回测评估指标

| 指标 | 含义 | 理想值 |
|------|------|--------|
| 年化收益率 | 策略年化收益 | >20% |
| 最大回撤 | 最大亏损幅度 | <15% |
| 夏普比率 | 风险调整收益 | >1.5 |
| 胜率 | 盈利交易占比 | >50% |

---

## 参考代码

完整回测代码见 `examples/backtest-example.py`
