# 回归分析与方法验证

## 回归分析

### 适用场景

创建变量间的函数关系、标准曲线拟合、预测。

### 核心函数

#### `linear_regression(x, y, force_zero=False)`
一元线性回归。支持强制过零点。

```python
from scripts.analysis.regression import linear_regression

# 常规线性回归
result = linear_regression(concentrations, responses)
# result["slope"], result["intercept"], result["r2"], result["syx"]

# 强制过原点
result = linear_regression(concentrations, responses, force_zero=True)
```

#### `polynomial_regression(x, y, degree=4)`
多项式回归拟合。

```python
from scripts.analysis.regression import polynomial_regression

# 4次多项式
result = polynomial_regression(x, y, degree=4)
```

#### `regression_stats(x, y, model_result)`
回归统计检验（调整R²、F值、残差方差）。

```python
from scripts.analysis.regression import regression_stats

stats = regression_stats(x, y, result)
```

#### `regression_plot(x, y, model_result, title="回归拟合图")`
回归拟合图 + 残差图。

### 输出

| 指标 | 说明 |
|------|------|
| `slope` / `intercept` | 斜率和截距 |
| `r2` | 判定系数 |
| `r` | 相关系数 |
| `Sy/x` | 剩余标准偏差 |
| `equation` | 回归方程文本 |
| `residuals` | 残差数组 |

---

## 方法验证指标

### 适用场景

检验检测行业的LOD/LOQ、回收率、不确定度计算。

### 核心函数

#### `calculate_lod_loq(calibration_data, method="pharmacopoeia")`
检出限和定量限计算。

```python
from scripts.analysis.validation import calculate_lod_loq

cal_data = {"x": [0, 5, 10, 15, 20], "y": [101, 32500, 66000, 91300, 133005]}
result = calculate_lod_loq(cal_data, method="pharmacopoeia")
# result["lod"], result["loq"], result["syx"], result["slope"]
```

支持的方法：
- `"pharmacopoeia"` — 药典法: LOD = 3.3×Sy/x / slope
- `"gbt27417"` — 国标法: LOD = 3×Sy/x / slope, LOQ = 9×Sy/x / slope

#### `calc_recovery(measured, spiked, blank=0)`
加标回收率计算。

```python
from scripts.analysis.validation import calc_recovery

result = calc_recovery([12.6, 8.3, 8.21], spiked=10, blank=0.5)
```

#### `uncertainty_propagation(calibration_data, sample_response, sample_count=1, std_curve_count=None, force_zero=False)`
标准曲线不确定度传递计算。

```python
from scripts.analysis.validation import uncertainty_propagation

cal = {"x": [0, 5, 10, 15, 20], "y": [101, 32500, 66000, 91300, 133005]}
result = uncertainty_propagation(cal, sample_response=[7236, 14904], 
                                  sample_count=2, force_zero=False)
```

### 方法验证指标一览

| 指标 | 公式 | 说明 |
|------|------|------|
| SD | $\sqrt{\frac{\sum(x_i-\bar{x})^2}{n-1}}$ | 标准偏差 |
| RSD | SD/mean × 100% | 相对标准偏差 |
| 合成SD | $\sqrt{\frac{\sum(n_i-1)SD_i^2}{\sum n_i - k}}$ | 多组精密度合并 |
| LOD(药典) | 3.3 × Sy/x / slope | 检出限 |
| LOD(GB/T 27417) | 3 × Sy/x / slope | 检出限 |
| LOQ(药典) | 10 × Sy/x / slope | 定量限 |
| LOQ(GB/T 27417) | 9 × Sy/x / slope | 定量限（= 3 × LOD） |
| 回收率 | (测得值-空白)/加标量 × 100% | 准确度 |
