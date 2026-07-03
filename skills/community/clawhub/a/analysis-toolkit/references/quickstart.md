# 快速使用

### 加载
```text
使用 分析质控工具包 做室内精密度分析
使用 分析质控工具包 做室间比对
```

### 导入
```python
# 场景函数（推荐，完整分析）
from scripts.scenarios.internal_qc import internal_precision_analysis, control_chart
from scripts.scenarios.interlab_qc import interlab_comparison, z_score_analysis
from scripts.scenarios.method_validation import calibration_curve, calc_lod_loq
from scripts.scenarios.trend_monitoring import monitoring_dashboard

# 细粒度算子（v2 新增）
from scripts.operations import (
    calc_mean, calc_sd, calc_rsd, calc_bias,
    calc_ubias, calc_u_combined, calc_expanded_u,
    calc_te_from_values, calc_te_judgment,
    calc_tcrit,
)
```

### 完整示例

```python
# 1. 加载数据
import pandas as pd
df = pd.read_excel("数据.xlsx")

# 2. 室内精密度分析
from scripts.scenarios import internal_qc
result = internal_qc.internal_precision_analysis(df, "水平", "结果")
print(result["synthetic_std"])  # 合成标准差

# 3. 质控图
fig, stats = internal_qc.control_chart(df, "结果")

# 4. 室间比对
from scripts.scenarios import interlab_qc
comp = interlab_qc.interlab_comparison(df, "实验室", "结果")
print(comp["conclusion"])

# 5. Z值分析
z_df = interlab_qc.z_score_analysis(df, "实验室", "结果")

# 6. 标准曲线
from scripts.scenarios import method_validation
curve = method_validation.calibration_curve(x, y)
lod_loq = method_validation.calc_lod_loq(calibration_data=curve, standard="gbt27417")
```

### 端到端完整流程（推荐顺序）

以下是从数据读取到生成报告的一次性完整流程。运行后即可获得所有分析结果。

```python
import pandas as pd
import matplotlib.pyplot as plt

# ── 0. 加载数据 ──
df = pd.read_excel("质控数据.xlsx")
print(f"数据概况: {df.shape[0]} 行 × {df.shape[1]} 列")
print(df.head())

# ── 1. 室内精密度分析 ──
from scripts.scenarios.internal_qc import internal_precision_analysis, control_chart
precision = internal_precision_analysis(df, group_col="水平", value_col="结果")
print("\n【精密度分析结果】")
print(f"  正规合成标准差: {precision['synthetic_std']:.4f}")
print(f"  简化合成标准差: {precision['synthetic_std_simple']:.4f}")
print(f"  两者偏差: {precision.get('verify_diff', 0)*100:.2f}%")
print(f"  RSD%: {precision.get('rsd', 0):.2f}%")
print(f"  各水平详情: {len(precision.get('per_level', []))} 个水平")

# ── 2. Levey-Jennings 质控图 ──
fig, stats = control_chart(df, value_col="结果")
print(f"\n【质控图统计】")
print(f"  均值: {stats['mean']:.4f}")
print(f"  SD: {stats['sd']:.4f}")
print(f"  超出±2σ: {stats.get('outside_2sigma', 0)} 点")
print(f"  超出±3σ: {stats.get('outside_3sigma', 0)} 点")
fig.savefig("质控图.png", dpi=150, bbox_inches="tight")

# ── 3. 输出摘要 ──
print("\n✅ 端到端分析完成")
print(f"  输出文件: 质控图.png")
```
