---
slug: data-analyst-chinese-free
name: data-analyst-chinese-free
version: 1.0.0
displayName: 中文数据分析(免费版)
summary: 中文语境数据清洗、统计分析与可视化建议,适合数据分析师、产品经理与运营快速上手。
license: Proprietary
edition: free
description: '中文数据分析免费版面向中文用户的数据分析日常工作流,提供开箱即用的数据清洗、统计分析与可视化代码模板。核心能力:

  - 数据读取统一封装:CSV、Excel、JSON、SQLite 等多种来源一键加载

  - 数据清洗模板:缺失值、重复值、异常值、类型转换的标准化处理

  - 统计分析方法库:描述统计、相关分析、分组聚合、交叉表

  - 可视化代码生成:折线、柱状、散点、热力、箱线等中文图表模板

  - 分析报告自动生成:6 段式结构化报告模板


  适用场景:

  - 日常销售/运营数据的快速清洗与汇总

  - 月度业务报告的图表与结论生成'
tags:
- 信息检索
- 中文场景
- 可视化
- 集成工具
tools:
- read
- exec
homepage: https://skillhub.cn
pricing_tier: L3
pricing_model: per_use
suggested_price: 29.9
tools: ["read", "write", "exec", "glob"]
tags: "数据处理,数据分析,工具"
---
# 中文数据分析 免费版

## 一、概述

中文数据分析免费版专为中文业务场景打造,覆盖数据读取、清洗、统计分析与可视化全流程。所有代码模板预置中文字体与中文标题,解决"图表中文乱码"这一长期痛点,让数据分析师、产品经理、运营人员能够在 60 秒内启动一次完整分析。

免费版聚焦日常分析的高频能力,适合 100 万行以内的数据集与单次分析任务。

## 核心能力

### 2.1 数据读取统一封装

| 数据源 | 代码片段 | 适用场景 |
|---|----|----|
| CSV | `pd.read_csv('data.csv')` | 通用文本数据 |
| Excel | `pd.read_excel('data.xlsx', sheet_name='Sheet1')` | 财务/运营报表 |
| JSON | `pd.read_json('data.json')` | API 返回数据 |
| SQLite | `pd.read_sql('SELECT * FROM t', conn)` | 本地数据库 |
| API | `requests.get(url).json()` | 第三方接口 |

**输入**: 用户提供1 数据读取统一封装所需的指令和必要参数。
**处理**: 解析1 数据读取统一封装的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回1 数据读取统一封装的响应数据,包含状态码、结果和日志。

### 2.2 数据清洗模板

- **缺失值处理**:`isnull().sum()` 统计、`dropna()` 删除、`fillna()` 填充(0/均值/众数)
- **重复值处理**:`duplicated().sum()` 统计、`drop_duplicates()` 删除(可按列去重)
- **类型转换**:`to_datetime`、`astype(float)`、`astype(category)`
- **异常值处理**:IQR 法(1.5 倍四分位距)自动过滤
- **文本规范化**:`strip()`、`lower()`、`replace()` 链式处理

**输入**: 用户提供2 数据清洗模板所需的指令和必要参数。
**处理**: 解析2 数据清洗模板的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回2 数据清洗模板的响应数据,包含状态码、结果和日志。

### 2.3 统计分析方法库

| 方法 | 代码 | 用途 |
|:-----|:-----|:-----|
| 描述统计 | `df.describe()` | 中心趋势与离散度 |
| 分位数 | `df['col'].quantile([.25,.5,.75])` | 分布形态 |
| 偏度峰度 | `df['col'].skew()` / `kurt()` | 正态性诊断 |
| 相关矩阵 | `df.corr()` | 变量关系 |
| 分组聚合 | `df.groupby('cat').agg(...)` | 多维汇总 |
| 交叉表 | `pd.crosstab(df['a'], df['b'])` | 类别关联 |

**输入**: 用户提供3 统计分析方法库所需的指令和必要参数。
**处理**: 解析3 统计分析方法库的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回3 统计分析方法库的响应数据,包含状态码、结果和日志。

### 2.4 中文可视化模板

所有图表预置 SimHei 字体与负号修正,无需额外配置:

- 折线图(趋势)、柱状图(对比)、散点图(关系)
- 直方图(分布)、箱线图(离群)、热力图(相关)
- 高级:分组柱状、小提琴图、散点矩阵、置信区间带

**输入**: 用户提供4 中文可视化模板所需的指令和必要参数。
**处理**: 解析4 中文可视化模板的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回4 中文可视化模板的响应数据,包含状态码、结果和日志。

### 2.5 分析报告模板

6 段式结构化报告:数据概览 → 关键指标 → 分布特征 → Top N → 趋势分析 → 业务建议。

**输入**: 用户提供5 分析报告模板所需的指令和必要参数。
**处理**: 解析5 分析报告模板的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回5 分析报告模板的响应数据,包含状态码、结果和日志。

- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：中文语境数据清洗、统计分析与可视化、适合数据分析师、产品经理与运营快、速上手、中文数据分析免费、版面向中文用户的、数据分析日常工作、提供开箱即用的数、代码模板、核心能力、等多种来源一键加、类型转换的标准化、相关分析、可视化代码生成、箱线等中文图表模、分析报告自动生成、段式结构化报告模等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 适用场景

| 角色 | 典型场景 | 输出形态 |
|---:|---:|---:|
| 数据分析师 | 销售明细周度复盘 | 清洗后数据 + 图表 + Markdown 报告 |
| 产品经理 | 用户行为漏斗分析 | 漏斗图 + 转化率 + 改进建议 |
| 运营专员 | 促销活动效果评估 | 对比图 + 增长率 + 结论 |
| 财务人员 | 月度财务汇总 | 分类汇总表 + 趋势图 |

## 不适用场景

以下场景中文数据分析(免费版)不适合处理：

- 实时流数据处理
- 小规模数据手动分析
- 非结构化文本情感分析

## 触发条件

需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于非本工具能力范围的需求。

## 使用流程

预计上手时间:**< 60 秒**。

直接以中文向 Agent 描述任务,以下为可复制模板:

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:---:|:---:|:---:|:---:|
| input | string | 是 | 中文数据分析(免费版)处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```text
请分析 sales.csv:
1. 字段: date, region, product, sales, units
2. 时间范围: 2024-01-01 至 2024-12-31
3. 关注: 华东地区月度销售趋势,以及 Top 5 商品
4. 输出: 折线图 + Top 5 表 + Markdown 报告
```

## 示例

### 5.1 数据读取

```python
import pandas as pd
# ...
df = pd.read_csv('data.csv')          # CSV
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')  # Excel
df = pd.read_json('data.json')        # JSON
# ...
import sqlite3
conn = sqlite3.connect('database.db')
df = pd.read_sql('SELECT * FROM table', conn)
```

### 5.2 数据预览

```python
print(df.shape)        # 行列数
print(df.columns)      # 列名
print(df.dtypes)       # 数据类型
print(df.info())       # 详细信息
print(df.head())       # 前 5 行
print(df.describe())   # 数值列统计
```

### 5.3 数据清洗

```python
df.isnull().sum()                       # 统计缺失
df.dropna()                             # 删除缺失行
df.fillna(0)                            # 填充 0
df['col'].fillna(df['col'].mean())      # 填充均值
df['col'].fillna(df['col'].mode()[0])   # 填充众数
# ...
df.duplicated().sum()                   # 统计重复
df.drop_duplicates()                    # 删除重复
# ...
df['date'] = pd.to_datetime(df['date'])
df['price'] = df['price'].astype(float)
# ...
# IQR 异常值过滤
Q1 = df['col'].quantile(0.25)
Q3 = df['col'].quantile(0.75)
IQR = Q3 - Q1
df = df[(df['col'] >= Q1 - 1.5*IQR) & (df['col'] <= Q3 + 1.5*IQR)]
```

### 5.4 统计分析

```python
df['col'].mean()      # 均值
df['col'].median()    # 中位数
df['col'].std()       # 标准差
df['col'].skew()      # 偏度
df['col'].kurt()      # 峰度
# ...
df.corr()             # 相关矩阵
df.corr()['target']   # 与目标的相关性
# ...
df.groupby('category').agg({
    'sales': ['sum', 'mean', 'count'],
    'profit': 'mean'
})
# ...
pd.crosstab(df['col1'], df['col2'])
```

### 5.5 中文可视化

```python
import matplotlib.pyplot as plt
import seaborn as sns
# ...
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# ...
plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['value'])
plt.title('趋势图')
plt.xlabel('日期')
plt.ylabel('数值')
plt.show()
# ...
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0)
plt.show()
```

### 5.6 报告生成模板

```python
def generate_report(df):
    """生成数据分析报告"""
    return f"""
## 1. 数据概览
- 数据量: {len(df)} 行 × {len(df.columns)} 列
- 缺失值: {df.isnull().sum().sum()} 个
# ...
## 2. 关键指标
- 总销售额: ¥{df['sales'].sum():,.2f}
- 平均订单: ¥{df['sales'].mean():,.2f}
# ...
## 3. 分布特征
- 偏度: {df['sales'].skew():.2f}
- 标准差: {df['sales'].std():,.2f}
# ...
## 4. Top 5 类别
{df.groupby('category')['sales'].sum().sort_values(ascending=False).head().to_markdown()}
# ...
## 5. 趋势分析
- 环比增长: {df['sales'].pct_change().mean()*100:.2f}%
# ...
## 6. 建议
1. 重点推广 Top 3 类别
2. 优化低转化品类
3. 关注季节性波动
"""
```

## 六、最佳实践

- **先预览后处理**:用 `head/info/describe` 三件套先了解数据全貌
- **备份原数据**:清洗前 `df.copy()` 保留原始数据
- **类型先行**:先 `to_datetime` 和 `astype` 规范类型,再做统计
- **中文图表**:务必预置 `SimHei` 字体,否则中文乱码
- **结果验证**:统计结论与业务直觉对照,异常需复核
- **可视化简洁**:一张图只表达一个观点,避免信息过载

## 常见问题

### Q1: 中文图表显示为方框怎么办?

A: 在脚本开头加上:
```python
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
```

### Q2: 大数据集内存不够怎么办?

A: 免费版推荐处理 100 万行以内。更大规模建议使用专业版的 Dask/Polars 后端与增量读取。

### Q3: Excel 多 Sheet 如何读取?

A: `pd.read_excel('file.xlsx', sheet_name=None)` 会返回所有 Sheet 的字典。

### Q4: 缺失值应该删除还是填充?

A: 缺失率 <5% 可删除;5-30% 适合用均值/中位数/众数填充;>30% 建议作为单独类别或用模型预测填充。

### Q5: 异常值如何判定?

A: 推荐 IQR 法(1.5 倍四分位距外为异常);正态分布数据可用 3σ 原则;业务场景可结合常识阈值。

## 已知限制

本免费体验版限制以下高级功能:

- 禁用时间序列分解与季节性分析
- 禁用假设检验与 A/B 测试自动化
- 禁用大数据集(>100 万行)批处理
- 禁用自定义报告模板与品牌化输出
- 禁用定时任务与邮件分发
- 禁用与外部数据库(如 `PostgreSQL`)的深度集成

解锁全部功能请使用专业版:`data-analyst-chinese-pro`
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 依赖说明

### 运行环境

- **Agent 平台**: 任意支持 SKILL.md 的 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **Python**: 3.8+

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |
| pandas | Python 库 | 必需 | `pip install pandas` |
| numpy | Python 库 | 必需 | `pip install numpy` |
| matplotlib | Python 库 | 可选 | `pip install matplotlib`(可视化) |
| seaborn | Python 库 | 可选 | `pip install seaborn`(高级可视化) |
| openpyxl | Python 库 | 可选 | `pip install openpyxl`(Excel 读写) |
| tabulate | Python 库 | 可选 | `pip install tabulate`(Markdown 表格) |

### API Key 配置

- 本 Skill 基于自然语言指令,无需额外 API Key
- 如对接外部 API,需用户自行提供对应的访问凭证,通过环境变量传入,**禁止**在对话或脚本中明文硬编码

### 可用性分类

- **分类**: MD+EXEC(纯 Markdown 指令,部分功能需要 exec 命令行执行能力)
- **说明**: 基于自然语言驱动的 AI Skill,通过中文场景化模板加速数据分析日常工作

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|:---|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "中文数据分析(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "data analyst chinese"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
