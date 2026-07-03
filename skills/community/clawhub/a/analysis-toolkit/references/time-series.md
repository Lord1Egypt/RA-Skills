# 时序分析与预测

## 适用场景

对时间序列数据进行聚合、趋势分析和未来预测。

- **质量监控**：阳性数/不合格数的日/周/月趋势
- **业务指标**：销售额、用户量的时序变化
- **风险预测**：基于历史数据预测未来走势
- **周期性分析**：发现数据中的周/月/季度周期

## 核心函数

### `time_trend_analyze(df, date_col, value_col, freq="D")`
时序聚合统计。按指定频率重采样并计算总值、均值等。

```python
from scripts.analysis.time_series import time_trend_analyze

ts = time_trend_analyze(df, "检测日期", "阳性数", freq="W")
```

### `trend_plot(ts_data, date_col, value_col, title="时序趋势图")`
趋势线绘制。

### `rolling_stats(ts_data, date_col, value_col, window=7)`
滚动统计量（滚动均值、标准差、上下限）。

### `prophet_forecast(df, date_col, value_col, group_col=None, periods=4, freq="W")`
基于Prophet 的时序预测。

```python
from scripts.analysis.time_series import prophet_forecast

# 多品类预测
forecast, fig = prophet_forecast(df, "检测日期", "阳性数", 
                                  group_col="品种", periods=6, freq="W")

# 整体预测
forecast, fig = prophet_forecast(df, "日期", "销售额", periods=12, freq="M")
```

### `prophet_plot(forecast, history, title)`
预测结果单独可视化。

### `trend_conclusion(ts_data, value_col, recent_n=7)`
自动生成趋势解读文本。

## 预测参数说明

| 参数 | 说明 | 默认 |
|------|------|------|
| `periods` | 预测期数 | 4 |
| `freq` | 粒度: "D"(日) / "W"(周) / "M"(月) / "Q"(季度) | "W" |
| `interval_width` | 置信区间宽度 | 0.95 |

## 依赖

需要安装 `prophet`:
```bash
pip install prophet
```

## 数据要求

日期列需为 `datetime` 类型，至少3个时间点才能预测。
