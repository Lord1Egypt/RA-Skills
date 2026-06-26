# 因子体系参考

## 因子列表（19个）

### 基本面因子（7个）

| 因子 | 说明 |
|------|------|
| `pe_ttm` | 市盈率（TTM） |
| `pb` | 市净率 |
| `roe` | 净资产收益率 |
| `dividend_yield` | 股息率 |
| `revenue_growth` | 营收增长率 |
| `profit_growth` | 净利润增长率 |
| eps_ttm | 每股收益动量 |

### 资金面因子（6个）

| 因子 | 说明 |
|------|------|
| `main_net_inflow` | 近5日主力净流入均值 |
| `northbound` | 北向资金持股比例变化 |
| `margin` | 融资余额变化率 |
| `vpt` | 量价趋势指标（20日斜率） |
| `mf_strength` | 大单净流入/总成交额 |
| `inst_holding` | 机构持仓比例变化 |

### 情绪面因子（6个）

| 因子 | 说明 |
|------|------|
| `turnover` | 换手率 |
| `volatility` | 波动率 |
| `limit_up_momentum` | 涨停动量 |
| `price_strength` | 价格强度 |
| `consecutive_up` | 连续上涨天数 |
| `news_sentiment` | 新闻情绪（东方财富股吧爬虫） |

## 因子合成

```python
from stock_skill.factors.base import FactorCombiner

# 等权合成
scores = FactorCombiner.equal_weight(factors)

# IC加权
scores = FactorCombiner.ic_weight(factors, ic_data)

# 最大化IC_IR（二次规划优化）
scores = FactorCombiner.maximize_ic_ir(factors, returns)
```

## 增强IC分析

`EnhancedFactorAnalyzer` 提供：

- **滚动IC** — 60日窗口滚动计算Spearman秩相关
- **IC衰减** — 计算1-20天延迟的IC，检测半衰期和持续性
- **因子换手率** — 衡量因子持仓稳定性
- **t统计量 + p值** — 判断IC是否显著

主流程中自动对 ma5/ma10/ma20/rsi/dif/dea/macd/k/d/boll_mid/atr 计算IC：

```json
{
  "rsi": {"ic": 0.035, "ic_ir": 0.42, "significant": true},
  "ma20": {"ic": 0.012, "ic_ir": 0.15, "significant": false}
}
```

显著性标准：|IC| > 0.02 且 |ICIR| > 0.3

## IC过滤机制

策略依赖的因子如果不显著，该策略的置信度自动降权：

| 情况 | 乘数 |
|------|------|
| 所有依赖因子显著 | ×1.0 |
| 部分因子不显著 | ×0.8 |
| 全部因子不显著 | ×0.6 |
| 无因子映射 | ×1.0 |

策略→因子映射：`rsi_oversold`→`rsi`, `kdj_cross`→`k,d`, `macd_cross`→`dif,dea,macd` 等

## 自定义因子

```python
from stock_skill.factors.base import Factor, register_factor

@register_factor
class MyFactor(Factor):
    name = "my_factor"
    category = "custom"
    description = "自定义因子"

    def compute(self, df, **kwargs):
        return some_value
```
