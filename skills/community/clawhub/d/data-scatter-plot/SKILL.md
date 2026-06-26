---
name: data-scatter-plot
description: 从CSV/Excel数据文件读取数据，根据Result行数据生成散点图，包含Min/Max Limit参考线
author: Matthew Hong
version: 1.0.1
---

# 数据散点图生成技能

## 功能描述

本技能用于处理数据文件（Excel/CSV），自动识别数据格式，并生成基于指定标题的散点图。

### 核心功能

1. **智能数据解析**：自动识别Item列、Result数据行、Min/Max Limit行
2. **动态散点图生成**：根据指定标题组合生成散点图
3. **Limit线绘制**：自动从数据中提取Min/Max Limit值并绘制参考线
4. **批量导出**：支持批量生成并保存为PNG图片

## 数据格式说明

### 输入文件格式（支持 .csv, .xls, .xlsx）

| 结构 | 说明 |
|------|------|
| 第1列 | Item名称（如 LESD3Z5.0CMT1HG） |
| 其他列 | 列标题（如 1 CONT2(V)） |
| Result行 | 散点图的数值数据来源 |
| Min Limit行 | 最小限制值 |
| Max Limit行 | 最大限制值 |

### 散点图标题命名规则

```
标题格式：'{第1列Item名称} + {对应列的列标题}'
示例：'LESD3Z5.0CMT1HG + 1 CONT2(V)'
```

### Y轴标签

- 取自对应列的 **Limit Unit**（如 mV, V, mA 等）

## 使用方法

### 基本用法

```python
from scripts.data_loader import ExcelDataLoader
from scripts.scatter_generator import ScatterPlotGenerator

# 1. 加载数据
loader = ExcelDataLoader('path/to/Test.xls')
data = loader.load()

# 2. 获取可用的散点图配置
configs = loader.get_scatter_configs()

# 3. 生成散点图
generator = ScatterPlotGenerator(output_dir='output/plots')
for config in configs:
    generator.generate(data, config)
```

### 命令行用法

```bash
python -m scripts.main --input Test.xls --output-dir output/plots
```

## 配置参数

### ScatterConfig 配置对象

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `item_name` | str | 是 | 第1列的Item名称 |
| `column_title` | str | 是 | 对应列的列标题 |
| `y_label` | str | 否 | Y轴标签（默认取Limit Unit） |
| `min_limit` | float | 否 | Min Limit值 |
| `max_limit` | float | 否 | Max Limit值 |
| `result_data` | List[float] | 是 | Result行数据 |

### 命令行参数

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--input` | `-i` | 输入数据文件路径（支持.csv/.xls/.xlsx） | 必需 |
| `--output-dir` | `-o` | 输出图片目录 | `./plots` |
| `--format` | `-f` | 输出格式 | `png` |
| `--dpi` | - | 图片分辨率 | `1200` |

## 输出示例

生成的散点图包含：
- 16:9 宽屏比例
- 主数据散点（蓝色圆点）
- **智能Limit线绘制**：
  - 只有Min Limit → 仅绘制Min Limit线
  - 只有Max Limit → 仅绘制Max Limit线
  - 两者都有 → 绘制两条线
  - 两者都没有 → 只绘制散点图
- Min Limit水平线（红色虚线，标注"Min Limit"）
- Max Limit水平线（红色虚线，标注"Max Limit"）
- X轴：数据点索引
- Y轴：对应Limit Unit
- 标题：'{Item名称} + {列标题}'

### 数据格式要求
- Result行及以下数据必须为**数值格式**（不支持文本格式）
- 支持带单位格式（如 "5mV"）自动提取数值部分

## 注意事项

1. **空值处理**：Result行中的空值会被自动跳过
2. **Limit行识别**：通过固定行名"Min Limit"和"Max Limit"识别
3. **文件编码**：CSV文件支持 UTF-8、GBK、GB2312、Latin1 自动识别
4. **依赖安装**：`pip install -r requirements.txt`

## 依赖清单

```
pandas>=1.5.0
matplotlib>=3.5.0
openpyxl>=3.0.0
xlrd>=2.0.0
```
