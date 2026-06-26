# 因子研究方法

## 简介

因子研究是量化投资的核心，通过挖掘有效因子构建选股策略。本指南基于视频第2、3、4集内容整理。

---

## 因子分类

### 1. 量价类因子

| 因子 | 名称 | 含义 |
|------|------|------|
| OBV | 能量潮 | 累加成交量判断资金流入流出 |
| MFI | 资金流量指标 | 成交量加权RSI |
| EMV | 波动指标 | 判断上涨是否轻松 |
| VAD | 威廉变异量 | 衡量多方/空方爆发力度 |

### 2. 趋势类因子

| 因子 | 名称 | 含义 |
|------|------|------|
| MOM | 动量 | 价格变化趋势 |
| RSI | 相对强弱 | 超买超卖判断 |
| MACD | 指数平滑异同 | 趋势判断 |

### 3. 反转类因子

| 因子 | 名称 | 含义 |
|------|------|------|
| VPT | 量价趋势指标 | 发现量价背离 |
| KDJ | 随机指标 | 超买超卖 |

### 4. 情绪类因子

| 因子 | 名称 | 含义 |
|------|------|------|
| VR | 成交量比率 | 情绪温度 |
| VRO3 | 成交量变化率 | 成交活跃度 |

---

## 因子计算

### TALib计算示例

```python
import talib
import pandas as pd

def calculate_factors(df):
    """计算量价因子"""
    factors = pd.DataFrame()
    factors['symbol'] = df['symbol']
    factors['trade_date'] = df['trade_date']
    
    # MFI资金流量
    factors['mfi'] = talib.MFI(
        df['high'], df['low'], df['close'], df['volume'],
        timeperiod=14
    )
    
    # RSI
    factors['rsi'] = talib.RSI(df['close'], timeperiod=14)
    
    # MACD
    factors['macd'], factors['macd_signal'], factors['macd_hist'] = \
        talib.MACD(df['close'])
    
    # OBV能量潮
    factors['obv'] = talib.OBV(df['close'], df['volume'])
    
    # 动量
    factors['mom'] = talib.MOM(df['close'], timeperiod=10)
    
    # 威廉变异量
    hl_diff = df['high'] - df['low']
    factors['wvad'] = ((df['close'] - df['low']) - (df['high'] - df['close'])) \
                      / hl_diff.replace(0, 1) * df['volume']
    
    return factors
```

---

## IC/IR/T值分析

### IC（信息系数）

**定义**：因子排序与未来收益排序的相关性

**解读**：
- IC > 0：因子与收益正相关
- IC < 0：因子与收益负相关（加负号后也可用）
- |IC|越大，预测能力越强

**计算方法**：
```python
import numpy as np

def calculate_ic(factor_values, future_returns):
    """计算IC值（Spearman相关系数）"""
    return np.corrcoef(
        factor_values.rank(),
        future_returns.rank()
    )[0, 1]
```

### IR（信息比率）

**定义**：IC均值 / IC标准差

**解读**：
- IR > 0.5：因子较稳定
- IR > 1：因子非常稳定
- IR < 0.3：因子不稳定，慎用

```python
def calculate_ir(ic_series):
    """计算IR"""
    return ic_series.mean() / ic_series.std()
```

### T值检验

**定义**：IC均值 / 均值标准误

**显著性判断**：
- |T| > 1.96：p < 0.05，显著
- |T| > 2.58：p < 0.01，极显著

```python
from scipy import stats

def calculate_t_value(ic_series):
    """计算T值"""
    n = len(ic_series)
    t_stat = ic_series.mean() / (ic_series.std() / np.sqrt(n))
    p_value = 2 * (1 - stats.t.cdf(abs(t_stat), n-1))
    return t_stat, p_value
```

---

## 多因子组合

### 权重分配

**方法一：IC加权**
```python
def ic_weight(factor_ics):
    """基于IC值分配权重"""
    total_ic = sum(abs(ic) for ic in factor_ics.values())
    weights = {k: abs(v) / total_ic for k, v in factor_ics.items()}
    return weights
```

**方法二：主观调整**
```python
# 根据市场风格调整因子权重
def adjust_weights(base_weights, market_regime):
    """
    market_regime: 'momentum' | 'reversal' | 'neutral'
    """
    if market_regime == 'momentum':
        base_weights['mom'] *= 1.5
        base_weights['rsi'] *= 0.5
    elif market_regime == 'reversal':
        base_weights['rsi'] *= 1.5
        base_weights['mom'] *= 0.5
    return normalize_weights(base_weights)
```

---

## 调仓频率选择

| 频率 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| 日频 | 响应快 | 成本高、滑点大 | 高频策略 |
| 周频 | 适中 | 响应较慢 | 大多数量化策略 |
| 月频 | 成本低 | 响应慢 | 长线策略 |

**建议**：对于散户和中长线投资者，推荐**5天或周度**调仓，不建议日频交易。

---

## 选股数量与效果

- 选20-30只：平衡分散与集中
- 选5只：过于集中，风险高
- 选50只以上：接近指数，效果不明显

---

## 盘中监控与评分系统

### 评分维度

```python
# 综合评分示例
def calculate_score(program_score, trend_score, strong_signal):
    """
    program_score: 程序指标分值
    trend_score: 趋势分值
    strong_signal: 是否强势 (0/1)
    """
    score = program_score * 0.4 + trend_score * 0.4 + strong_signal * 20
    return min(max(score, 0), 100)
```

### 信号文件格式

```csv
symbol,program_score,trend_score,strong,date,score
000001.SZ,75,82,1,2025-01-02,81
600000.SH,68,71,0,2025-01-02,59
```

---

## 注意事项

1. **避免未来函数**：使用T日收盘因子值，只能用T+1日收益
2. **IC动态变化**：IC低的因子会被自动降低权重
3. **市场风格切换**：根据市场状态调整因子权重
4. **样本外检验**：回测结果需在样本外验证
