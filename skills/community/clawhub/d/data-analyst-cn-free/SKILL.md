---
slug: "data-analyst-cn-free"
name: "data-analyst-cn-free"
version: "1.0.0"
displayName: "数据分析师(免费版)"
summary: "基础数据清洗、描述统计与基础可视化代码生成，支持CSV与Excel读取。数据分析师免费版，提供基础的数据清洗与统计分析能力. 核心能力包括： - CSV与Excel数据读取（pd.read_"
summary_zh: "基础数据清洗、描述统计与基础可视化代码生成，支持CSV与Excel读取。数据分析师免费版，提供基础的数据清洗与统计分析能力. 核心能力包括： - CSV与Excel数据读取（pd.read_"
license: "MIT"
description: "|-. 适用于需要data analyst cn相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性."
  数据分析师免费版，提供基础的数据清洗与统计分析能力.
  核心能力包括：
  - CSV与Excel数据读取（pd.read_csv、pd.read_excel）
  - 数据预览（shape、dtypes、describe、head、tail）
  - 基础数据清洗（缺失值填充、去重、类型转换）
  - 描述统计（均值、中位数、标准差、分位数）
  - 基础可视化（折线图、柱状图、散点图、直方图）
  高级功能（IQR异常值剔除、时间序列分析、高级图表、分析报告生成）为付费版专享.
tags:
  - 信息检索
  - analyst
  - automation
  - productivity
  - data-analysis
  - visualization
  - 数据处理
  - 数据分析
  - 工具
  - plt
tools:
  - read
  - exec
  - write
  - glob
homepage: ""
category: "Research"
pricing_tier: free
---
# 数据分析师（免费版）

## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 数据分析师(免费版)处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 概述

快速进行基础数据清洗、统计分析和可视化，适合数据分析师、产品经理、运营人员的日常数据处理需求.
## 核心能力
### 数据读取
```python
import pandas as pd
# ...
df = pd.read_csv('data.csv')
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')
```

> **升级提示**：JSON、SQLite数据库、API接口数据读取为付费版专享功能.

### 数据预览
```python
print(df.shape)        # 行列数，如 (1542, 7)
print(df.columns)      # 列名列表
print(df.dtypes)       # 数据类型
print(df.head())       # 前 5 行
print(df.describe())   # 数值列统计
```

- 异常时参考错误处理章节进行恢复
- 关键参数: `数据预览` 选项

### 数据清洗
**缺失值处理**：

```python
df.isnull().sum()                    # 统计缺失
df.dropna()                          # 删除缺失行
df.fillna(0)                         # 填充 0
df.fillna(df.mean())                 # 填充均值
```

**去重处理**：

```python
df.duplicated().sum()                # 统计重复
df.drop_duplicates()                 # 删除重复
```

**类型转换**：

```python
df['date'] = pd.to_datetime(df['date'])
df['price'] = df['price'].astype(float)
```

> **升级提示**：IQR异常值剔除（`Q1 - 1.5*IQR` 至 `Q3 + 1.5*IQR`）、字符串处理（strip/lower/replace）为付费版专享功能.

### 描述统计
```python
df['col'].mean()      # 均值
df['col'].median()    # 中位数
df['col'].std()       # 标准差
df['col'].quantile([0.25, 0.5, 0.75])  # 分位数
```

> **升级提示**：偏度（`skew`）、峰度（`kurt`）、相关矩阵（`corr`）、分组聚合（`groupby.agg`）、交叉表（`crosstab`）为付费版专享功能.

### 基础可视化

**中文字体配置**（必须先执行）：

```python
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
```

| 图表类型 | 代码 | 适用场景 |
|:-----|:-----|:-----|
| 折线图 | `plt.plot(df['date'], df['value'])` | 趋势变化 |
| 柱状图 | `plt.bar(df['category'], df['value'])` | 分类对比 |
| 散点图 | `plt.scatter(df['x'], df['y'], alpha=0.5)` | 关系分布 |
| 直方图 | `plt.hist(df['value'], bins=20, edgecolor='black')` | 分布形态 |

> **升级提示**：箱线图（`sns.boxplot`）、热力图（`sns.heatmap`）、小提琴图、成对关系图、多轴趋势图为付费版专享功能。时间序列分析（`resample`、`rolling`、`seasonal_decompose`）为付费版专享功能。分析报告自动生成为付费版专享功能.
#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
需要配置对应API Key，详见上文环境配置章节

### 可用性分类
- **分类**: MD+EXEC（）

**API Key配置方式**:
```bash
export API_KEY=${API_KEY:?请设置环境变量}
```
配置后需重启会话或开启新终端生效。API Key应妥善保管,避免泄露到版本控制系统.
## 使用流程

1. **读取数据**：使用 `pd.read_csv()` 或 `pd.read_excel()` 加载数据
2. **预览检查**：执行 `df.shape`、`df.dtypes`、`df.describe()` 了解数据全貌
3. **数据清洗**：处理缺失值（`fillna`）、去重（`drop_duplicates`）、类型转换（`astype`）
4. **统计分析**：计算均值、中位数、标准差等描述统计量
5. **可视化**：配置SimHei字体后生成基础图表代码

**结果验证**: 任务完成后,查看输出确认状态。成功时返回摘要和数据;失败时根据错误信息排查,参考恢复章节获取修复步骤.
## 示例

### 示例1：CSV数据清洗与统计

```text
输入: 分析这个 CSV 文件：sales.csv
# ...
处理:
- df = pd.read_csv('sales.csv')
- 缺失值: df['sales'].fillna(df['sales'].mean())
- 统计: 均值¥45,230, 中位数¥38,500, 标准差¥12,400
# ...
输出: 1542 行数据，销售额均值¥45,230
```

### 示例2：生成折线图代码

```text
输入: 为这些数据生成折线图代码
# ...
输出:
plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['value'])
plt.title('趋势图')
plt.xlabel('日期')
plt.ylabel('数值')
plt.show()
```

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 中文图表显示方框 | 未配置SimHei字体 | 执行 `plt.rcParams['font.sans-serif'] = ['SimHei']` 和 `plt.rcParams['axes.unicode_minus'] = False` |
| `KeyError` 列名不存在 | 列名含空格或大小写不一致 | 先 `print(df.columns)` 检查实际列名 |
| `fillna(df.mean())` 报错 | 含非数值列无法求均值 | 仅对数值列填充：`df.select_dtypes(include='number').fillna(df.mean())` |
| `astype(float)` 转换失败 | 列中含非数字字符串 | 使用 `pd.to_numeric(df['col'], errors='coerce')` 将非法值转为NaN |
| 大数据集内存溢出 | DataFrame超过可用内存 | 使用 `dtype` 参数指定类型，或分块读取 |

## 常见问题

### Q1: 图表中中文显示为方框怎么解决？
A: 在绘图前配置字体：`plt.rcParams['font.sans-serif'] = ['SimHei']`（Windows），同时设置 `plt.rcParams['axes.unicode_minus'] = False`.
### Q2: 如何处理异常值？
A: IQR异常值剔除方法为付费版专享功能。免费版可使用 `df.describe()` 查看最大最小值，手动过滤极端值.
### Q3: 如何做时间序列分析？
A: 时间序列分析（`resample`、`rolling`、`seasonal_decompose`）为付费版专享功能。免费版可手动按月份分组计算统计量.
### Q4: 如何生成分析报告？
A: 分析报告自动生成（`generate_report()`）为付费版专享功能。免费版可手动使用 `df.describe()` 和 `df.info()` 查看数据概况.
### Q5: 如何读取JSON或数据库数据？
A: JSON、SQLite数据库、API接口数据读取为付费版专享功能。免费版支持CSV和Excel格式读取.
## 已知限制

- 免费版不支持JSON、SQLite、API数据源读取
- 免费版不包含IQR异常值剔除与字符串处理
- 免费版不包含时间序列分析（resample、rolling、seasonal_decompose）
- 免费版不包含高级可视化（箱线图、热力图、小提琴图等）
- 免费版不包含分析报告自动生成
- 不适用于实时流数据处理
- 升级至付费版可解锁全部高级功能
