# 流水线（Pipeline）


这个工具箱支持四种用法，从简单到灵活：

- **单独用（Standalone）** — 单步调用一个算子或场景函数
- **组合用（Ad-hoc Pipeline）** — 用 `pipeline()` + `step()` 临时拼一个流程
- **按场景用（Template Pipeline）** — 加载内置模板，跑完整场景
- **自扩展（Auto-expand）** — 查标准后自动补全算子、注册模板

### 四层架构（v2）

```
┌──────────────────────────────────────────────┐
│ 4. 自扩展层                                      │
│    查标准 → 自动补全算子 → 生成模板 → 注册复用     │
├──────────────────────────────────────────────┤
│ 3. 单独调用层 — 单算子调用                      │
│    calc_mean(x), calc_sd(x), calc_te(...)    │
├──────────────────────────────────────────────┤
│ 2. 组合层 — Pipeline 编排                     │
│    a) 临时组合 (Ad-hoc)                       │
│    b) 模板场景 + HTML报告包 (Template)          │
├──────────────────────────────────────────────┤
│ 1. 细粒度算子层 (scripts/operations/)         │
│    statistics | uncertainty | total_error     │
│    viz (可视化算子: metric_card, te_breakdown…) │
└──────────────────────────────────────────────┘
```

### 模板 = 场景 + HTML 报告包（v2 核心）

每个模板不再只是计算步骤的组合，而是**完整的场景+报告包**：

```
┌── 模板库 ─────────────────────────────┐
│                                        │
│  templates/default/   (场景分析模板)      │
│  ├── 室内质控全流程.json   steps: [...]  │
│  ├── 总误差评估.json       steps: [...]  │
│  │   └── default_report: "总误差报告"   │ ← 关联特色报告
│  └── 测量不确定度评定.json  steps: [...]  │
│      └── default_report: "测量不确定度报告"│
│                                        │
│  templates/reports/   (可视化报告模板)    │
│  ├── 总误差报告.json      sections: [...]│
│  └── 测量不确定度报告.json sections: [...]│
│                                        │
│  templates/user/   (用户自定义)          │
└────────────────────────────────────────┘
```

**场景 vs 报告 —— 两种不同的模板，独立但可组合：**

| 维度 | 场景模板 | 报告模板 |
| ------ |---------| --------- |
| 算子类型 | 数学/统计算子 (calc_mean, calc_te) | 可视化算子 (metric_card, te_breakdown) |
| 产出 | 数值 results dict | HTML 报告片段 |
| 存储 | `templates/default/` | `templates/reports/` |
| 默认关联 | 通过 `default_report` 字段指定 | 无 |

一个场景的 results 可以被多个报告模板消费：
```python
# 默认报告
html = render_from_template("总误差评估", results)

# 同一结果，换一个报告
custom = {"title":"快报","sections":[...]}
html2 = render_report(custom, results)
```

### 可视化算子（可扩展）

可视化算子位于 `scripts/operations/viz.py`，与分析算子一样可独立注册和扩展：

| 算子 | 用途 |
| ------ |------|
| `metric_card()` | 关键指标卡片组 |
| `data_table()` | key-value 数据表 |
| `bar_chart()` / `pie_chart()` | 通用图表 |
| `te_breakdown()` | 总误差分量分解图 |
| `te_judgment_section()` | 总误差判定结果卡片 |
| `measurement_uncertainty_section()` | 合成/扩展不确定度报告 |

自定义 section 类型可通过 `register_section_type()` 注册：

```python
from scripts.reporting.report_engine import register_section_type
register_section_type("my_chart", my_render_func)
```
