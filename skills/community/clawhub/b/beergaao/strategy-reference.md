# 策略引擎参考

## 传统策略（10种，均含买入+卖出信号）

| 策略 | 买入条件 | 卖出条件 |
|------|---------|---------|
| `ma_breakout` | 均线多头 + 放量突破 | 跌破MA20 / 均线空头排列 |
| `macd_cross` | MACD金叉，柱状线转正 | MACD死叉，柱状线缩小 |
| `boll_squeeze` | 布林收口后突破中轨 | 跌破布林下轨 |
| `rsi_oversold` | RSI从超卖区反弹 | RSI从超买区回落 |
| `kdj_cross` | KDJ超卖区金叉 | KDJ超买区死叉 |
| `volume_shrink` | 上升趋势缩量回调 | 放量下跌跌破均线 |
| `vol_price_divergence` | 底背离（价跌量增） | 顶背离（价涨量缩） |
| `obv_trend` | OBV上升确认资金流入 | OBV下降确认资金流出 |
| `double_ma` | MA5/MA20金叉放量 | MA5/MA20死叉 |
| `support_bounce` | 触及支撑后反弹 | 跌破MA60/布林下轨支撑 |

## 机器学习策略（4种 + 集成）

### 模型类型

| 模型 | 算法 | 关键参数 |
|------|------|----------|
| XGBoost | Gradient Boosting | n_estimators=100, max_depth=5, lr=0.1 |
| LightGBM | LightGBM | n_estimators=100, max_depth=5, lr=0.1 |
| 随机森林 | Random Forest | n_estimators=200, max_depth=8 |
| MLP | 神经网络 | hidden_layers=(64,32,16), adam优化器 |

### 特征工程（40+维，纯技术指标）

| 类别 | 特征 | 说明 |
|------|------|------|
| 均线 | ma_5/10/20/60, ma_slope, close_ma_ratio | 均线值、斜率、价格偏离度 |
| RSI | rsi_6, rsi_14 | 6日和14日RSI |
| 波动率 | volatility_10/20 | 10日/20日波动率 |
| 成交量 | volume_ratio_5/10, volume_change | 量比、量变化率 |
| 动量 | momentum_5/10/20 | 5/10/20日收益率 |
| MACD | dif, dea, macd, macd_cross | MACD指标及金叉信号 |
| 布林带 | boll_width, boll_position | 带宽、价格在带内位置 |
| K线形态 | price_range, upper_shadow, lower_shadow | 振幅、上下影线 |
| 滞后 | return_lag_1/2/3/5, volume_lag | 历史收益率和量变化 |

**标签定义**：未来5日收益率 > +2% 为买入(1)，< -2% 为卖出(-1)，否则持有(0)

### 训练方式

- **最低样本量**：200条K线（约10个月日线）
- **增量训练**：支持 `incremental_train()`，在已有模型上追加训练
- **模型持久化**：`save_model()`/`load_model()` 自动保存到 `models/` 目录
- **集成融合**：4模型加权投票，权重由训练准确率决定

### 防过拟合措施

| 措施 | XGBoost/LightGBM | 随机森林 | MLP |
|------|------------------|----------|-----|
| 树深度限制 | max_depth=5 | max_depth=8 | - |
| 子采样 | subsample=0.8 | - | batch_size=32 |
| 特征采样 | colsample_bytree=0.8 | - | - |
| 叶子节点 | - | min_samples_split=10, min_samples_leaf=5 | - |
| 正则化 | - | - | alpha=0.001 (L2) |

### 集成ML策略

```python
from stock_skill.strategies.ml_strategies import EnsembleMLStrategy

ml = EnsembleMLStrategy()
ml.train(df, forward_periods=5, threshold=0.02)
signal = ml.predict(df)  # 返回 MLSignal(direction, confidence, ...)
```

集成策略自动：
1. 训练4个模型并计算准确率
2. 按准确率分配投票权重
3. 加权投票融合，阈值 > 0.3 才输出信号

## 集成引擎

- **市场状态检测** — ADX趋势强度 + 波动率，自动识别 trend_up/trend_down/range/volatile
- **动态权重** — 按市场状态和历史胜率调整各策略权重
- **信号去冗余** — 同族策略（如MA系3个）只取最高置信度代表
- **IC过滤** — 因子显著性评估，低质量因子对应的策略自动降权（×0.6~1.0）

## 参数校准

`StrategyCalibrator` 基于历史K线自动搜索最优参数：

```python
from stock_skill.strategies.strategies import StrategyCalibrator

# 全量校准
results = StrategyCalibrator.calibrate(df)

# 按市场状态分别校准
results = StrategyCalibrator.calibrate(df, regime="trend")
results = StrategyCalibrator.calibrate_all_regimes(df)
```

可校准参数：RSI阈值(20-40)、KDJ阈值(30-60)、成交量倍数(1.2-2.3)、布林收口比(0.90-0.99)等

## 信号融合权重

| 信号源 | 权重 | 说明 |
|--------|------|------|
| 传统策略(去重后) | 0.45 | 按历史胜率动态调权 |
| 集成引擎 | 0.30 | 市场状态检测+动态权重 |
| ML策略 | 0.25 | 4模型集成投票 |

## 策略相关性分组

```
ma_family:  {ma_breakout, double_ma, volume_shrink}
macd_family: {macd_cross}
boll_family: {boll_squeeze}
rsi_family:  {rsi_oversold}
kdj_family:  {kdj_cross}
vol_family:  {vol_price_divergence, obv_trend}
support_family: {support_bounce}
```

同族策略同时触发时只计1票，避免信号膨胀。

## 参数优化

```python
from stock_skill.strategies.optimizer import StrategyOptimizer, WalkForwardOptimizer

optimizer = StrategyOptimizer(MABreakoutStrategy)
optimizer.add_param("vol_multiplier", "float", low=1.0, high=3.0)
result = optimizer.bayesian_optimization(df, n_trials=50)
```

支持：网格搜索、随机搜索、贝叶斯优化、遗传算法、Walk-Forward、集成优化

## 滚动窗口回测

Walk-Forward 分析：在训练窗口调参，在测试窗口验证，滚动推进评估策略稳定性。

```python
from stock_skill.backtest.engine import RollingBacktestEngine, BacktestConfig

# 初始化滚动回测引擎
engine = RollingBacktestEngine(
    window_size_days=252,  # 训练窗口：1年
    step_days=21,          # 滚动步长：1个月
    config=BacktestConfig(initial_capital=1_000_000),
)

# 定义参数优化器（在训练窗口内调参）
def optimize_params(train_data):
    # 使用 StrategyOptimizer 优化参数
    from stock_skill.strategies.strategies import MABreakoutStrategy
    from stock_skill.strategies.optimizer import StrategyOptimizer

    optimizer = StrategyOptimizer(MABreakoutStrategy)
    optimizer.add_param("vol_multiplier", "float", low=1.0, high=3.0)
    result = optimizer.bayesian_optimization(train_data["600036.SH"], n_trials=20)
    return result.best_params, result.best_score

# 运行滚动回测
result = engine.run(
    stock_data=stock_data,
    signal_func=my_signal_func,
    param_optimizer=optimize_params,
    start_date="2023-01-01",
    end_date="2026-01-01",
)

# 输出结果
print(result.summary())
print(result.to_dict())
```

### 输出指标

| 指标 | 说明 |
|------|------|
| avg_sharpe | 所有窗口的平均夏普比率 |
| avg_win_rate | 所有窗口的平均胜率 |
| avg_return | 所有窗口的平均收益 |
| avg_max_drawdown | 所有窗口的平均最大回撤 |
| sharpe_std | 夏普比率标准差（越小越稳定） |
| win_rate_std | 胜率标准差 |
| drawdown_std | 回撤标准差 |
| best_window | 表现最好的窗口 |
| worst_window | 表现最差的窗口 |
