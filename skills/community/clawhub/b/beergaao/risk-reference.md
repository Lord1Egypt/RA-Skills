# 风控与回测参考

## 风控体系

### 止损（三选最严）

| 类型 | 计算方式 |
|------|---------|
| 固定止损 | 价格 × (1 + STOP_LOSS_RATE)，默认 -4% |
| ATR止损 | 价格 - 2×ATR |
| 支撑位止损 | 支撑位 × 0.98 |

### 止盈（三选最近）

| 类型 | 计算方式 |
|------|---------|
| 基础目标 | 价格 × (1 + TARGET_RATE)，默认 +6% |
| ATR目标 | 价格 + 3×ATR |
| 压力位目标 | 阻力位价格 |

### 移动止损

`TrailingStop` — 最高价回撤 2×ATR 时触发，止损线只上移不下移

### 仓位管理

```
仓位 = 基础仓位 × 市场因子 × 置信度因子 × ATR因子
```

| 因子 | 计算 |
|------|------|
| 基础仓位 | MAX_SINGLE_POSITION / 信号数 |
| 市场因子 | 情绪≥8→1.3, ≥6→1.1, ≥4→0.8, ≥2→0.5 |
| 置信度因子 | min(置信度/0.6, 1.5) |
| ATR因子 | ATR/价格>4%→0.7, >3%→0.85 |

### 相关性风控

检测组合内资产相关系数，超过阈值（默认0.7）时告警

### 熔断机制

| 触发条件 | 说明 |
|---------|------|
| 跌停潮 | 跌停股数 > 30 |
| 极端弱势 | 情绪分 < 2/10 |
| 普跌 | 下跌占比 > 90% |

## 专业回测引擎

`BacktestEngine` 支持：

| 特性 | 说明 |
|------|------|
| 复权处理 | 前复权/后复权（需adj_factor列） |
| 涨跌停限制 | 涨停封板不可买入，跌停封板不可卖出 |
| T+1约束 | 今日买入明日才能卖出 |
| 成交量约束 | 最大参与率10% |
| 成交本模型 | 佣金万三（最低5元）+ 印花税千一 + 滑点（固定/百分比/成交量冲击） |
| 基准对比 | Alpha/Beta/信息比率/跟踪误差 |
| 指标 | 总收益/年化收益/最大回撤/夏普/索提诺/卡尔马/胜率/盈亏比 |

### 快速回测

`_run_backtest(df)` — 在 `analyze_stock` 中自动运行，返回胜率/夏普/盈亏比

### 专业回测

```python
from stock_skill.backtest.engine import BacktestEngine, BacktestConfig, CostModel

config = BacktestConfig(
    initial_capital=1_000_000,
    cost_model=CostModel(commission_rate=0.0003, stamp_tax_rate=0.001),
    enforce_t1=True,
    enforce_limit=True,
    enforce_volume=True,
)
engine = BacktestEngine(config)
metrics = engine.run(stock_data, signal_func, benchmark_data=bm_df)
```

## 绩效追踪

### 信号回填

`evaluate_signal_performance` — 回填近10天未记录的信号实际收益：

- 计算 1d/3d/5d/10d 收益率
- 判断是否触发止损/止盈
- 写入 `signal_performance` 表
- 刷新集成引擎的策略权重

### 策略归因

`strategy_attribution(days=30)` — 追踪收益来源：

```json
{
  "attributions": [
    {"strategy": "macd_cross", "signals": 15, "win_rate": 0.67, "avg_return_5d": 0.023, "contribution": 0.23},
    {"strategy": "rsi_oversold", "signals": 8, "win_rate": 0.75, "avg_return_5d": 0.018, "contribution": 0.11}
  ]
}
```

贡献度 = 胜率 × 均收益 × 信号数

## 交易成本

| 项目 | 费率 |
|------|------|
| 佣金 | 万三（双向，最低5元） |
| 印花税 | 千一（卖出） |
| 滑点 | 固定/百分比/成交量冲击 三种模型 |

## Brinson归因

```python
from stock_skill.attribution.brinson import BrinsonModel

result = BrinsonModel.single_period(
    portfolio_weights={"tech": 0.4, "finance": 0.3},
    benchmark_weights={"tech": 0.3, "finance": 0.4},
    portfolio_returns={"tech": 0.05, "finance": 0.02},
    benchmark_returns={"tech": 0.03, "finance": 0.04},
)
# 配置效应 + 选择效应 + 交互效应
```
