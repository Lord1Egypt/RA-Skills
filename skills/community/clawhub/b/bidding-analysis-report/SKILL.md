---
name: bidding-analysis-report
version: 1.0.0
description: 招标数据分析报告生成技能 - 支持AI项目占比分析、年度趋势分析、TOP机构排名，自动生成Word/PDF报告，嵌入高质量图表。适用于高校招标、政府采购、企业采购等场景。
metadata:
  short-description: 招标数据分析报告生成，支持AI项目占比分析、年度趋势、TOP排名，输出Word/PDF报告
  openclaw:
    slug: bidding-analysis-report
    license: MIT
    homepage: https://github.com/openclaw/bidding-analysis-report
---

# 招标数据分析报告生成技能

## 功能概述

本技能用于分析招标数据并生成专业报告，支持：

1. **AI项目占比分析** - 计算AI相关招标项目数和金额占比
2. **年度趋势分析** - 分析多年度项目数和金额变化趋势
3. **TOP机构排名** - 统计招标项目数/金额排名前N的机构
4. **分机构详细分析** - 每个机构的年度趋势和拓展建议
5. **图表自动生成** - 嵌套环形图、百分比柱状图
6. **报告输出** - Word格式（推荐）或PDF格式

---

## 使用场景

- 高校招标数据分析
- 政府采购AI项目统计
- 企业采购趋势分析
- 行业招标报告生成

---

## 输入要求

### 数据格式
Excel文件（.xlsx），需包含以下字段：
- `项目名称` - 招标项目名称
- `项目主体` - 项目分类/类型
- `成交金额（元）` - 中标金额
- `信息采集日期` - 招标日期（时间戳或日期格式）
- `甲方名称` - 招标机构名称

### AI项目识别
默认关键词：`人工智能`、`AI`、`智能`、`大数据`、`机器学习`、`深度学习`、`智慧`

---

## 输出格式

### Word报告（推荐）
- 字体：微软雅黑（或系统支持的 Droid Sans Fallback）
- 行距：1.5倍行距
- 图表：嵌入PNG图片，居中显示
- 关键数据：加粗显示

### 图表类型
1. **嵌套环形图** - 外环项目数占比，内环金额占比
2. **百分比柱状图** - 年度趋势对比

### 配色方案（明亮科技风）
- AI项目数：亮橙色 `#FF8C42`
- AI金额：青色 `#00F5D4`
- 其他项目：亮蓝色 `#7ED4FF`
- 其他金额：蓝色 `#00D4FF`

---

## 使用方法

### 基本用法
```python
from bidding_analysis_report import BiddingReport

# 创建报告实例
report = BiddingReport(
    data_path='招标数据.xlsx',
    ai_keywords=['人工智能', 'AI', '智能', '大数据'],
    output_format='word'  # 或 'pdf'
)

# 生成报告
report.generate(
    title='昆明高校近三年AI项目分析报告',
    top_n=10,  # TOP机构数量
    detail_n=5  # 详细分析的机构数量
)
```

### 命令行用法
```bash
python bidding_report.py \
  --data 招标数据.xlsx \
  --title "昆明高校AI招标分析报告" \
  --output report.docx \
  --top 10 \
  --detail 5
```

---

## 报告结构

### 一、总体情况
1. AI项目数占比、金额占比（嵌套环形图）
2. 年度发展趋势分析（百分比柱状图）

### 二、TOP机构
- 项目数占比最高的N个机构列表
- 包含：机构名称、总招标数、招标总金额、AI项目数、AI金额
- 结合机构特点分析AI项目关联

### 三、分机构详细情况
每个机构包含：
1. 近3年招标项目总数及金额、AI项目数及金额（嵌套环形图）
2. 分年度AI项目趋势分析（百分比柱状图）
3. 拓展建议

---

## 技术实现

### 依赖库
```
pandas>=1.3.0
matplotlib>=3.5.0
python-docx>=0.8.11
openpyxl>=3.0.0
```

### 中文字体配置
```python
import matplotlib.pyplot as plt

# 优先使用微软雅黑，回退到系统支持字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'Droid Sans Fallback', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False
```

### 图表生成
```python
# 嵌套环形图
fig, ax = plt.subplots(figsize=(12, 8))
wedges1 = ax.pie(outer_vals, radius=1.3, colors=colors_outer,
                  wedgeprops=dict(width=0.35, edgecolor='white'))
wedges2 = ax.pie(inner_vals, radius=0.95, colors=colors_inner,
                  wedgeprops=dict(width=0.35, edgecolor='white'))

# 保存为PNG
plt.savefig('chart.png', dpi=150, bbox_inches='tight', facecolor='white')
```

### Word文档生成
```python
from docx import Document
from docx.shared import Inches, Pt

doc = Document()

# 设置字体和行距
style = doc.styles['Normal']
style.font.name = 'Microsoft YaHei'
style.font.size = Pt(12)

# 插入图表
doc.add_picture('chart.png', width=Inches(5.5))

# 数据加粗显示
p = doc.add_paragraph()
p.add_run('总项目数：')
run = p.add_run('6,786')
run.bold = True
```

---

## 配置选项

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `data_path` | 数据文件路径 | 必填 |
| `ai_keywords` | AI项目识别关键词 | ['人工智能','AI','智能',...] |
| `output_format` | 输出格式 | 'word' |
| `top_n` | TOP机构数量 | 10 |
| `detail_n` | 详细分析机构数量 | 5 |
| `chart_dpi` | 图表分辨率 | 150 |
| `line_spacing` | 行距倍数 | 1.5 |

---

## 注意事项

1. **中文字体**：优先使用微软雅黑，系统不支持时自动回退到 Droid Sans Fallback
2. **数据格式**：确保Excel文件包含必需字段，日期字段需可解析
3. **图表嵌入**：Word格式推荐，PDF格式中文字体支持有限
4. **数据填充**：使用 `.format()` 或字符串拼接，避免 f-string 编码问题

---

## 示例输出

### 昆明高校AI招标分析报告（2023-2026）

**总体情况**：
- 总招标项目：6,786项
- AI相关项目：1,193项（占比 17.6%）
- 总招标金额：96亿元
- AI项目金额：15亿元（占比 15.6%）

**年度趋势**：
- 2023年：AI项目占比 14.8%
- 2024年：AI项目占比 16.8%
- 2025年：AI项目占比 20.7%
- 2026Q1：AI项目占比 15.7%

**TOP10高校**：
1. 云南大学 - AI项目61项
2. 昆明理工大学 - AI项目54项
3. 云南开放大学 - AI项目33项
...

---

## 更新日志

### v1.0.0 (2026-04-21)
- 初始版本发布
- 支持AI项目占比分析
- 支持年度趋势分析
- 支持TOP机构排名
- 支持Word/PDF报告输出
- 嵌套环形图和百分比柱状图
- 明亮科技风配色方案

---

**作者**: OpenClaw Team  
**许可**: MIT License
