---
name: achievement-qztc
description: 课程目标达成情况分析表生成工具 v5.3（仅供QZTC内部使用）。Generator+Reviewer双模式，支持Pipeline一键生成+审查。权重和目标配置均从模板动态读取。
---

# 课程目标达成情况分析表生成工具 v5.3

> 🎯 **设计模式**: Generator + Reviewer + Pipeline
> 📁 **代码文件**: `achievement_generator.py`
> 🔍 **审查脚本**: `scripts/review_document.py`
> 📖 **公式参考**: `references/grading-formula.md`

---

## 🚀 快速开始

### Pipeline 一键执行（推荐）

```bash
# 生成 + 审查（自动执行）
python3 achievement_generator.py --pipeline "C#程序设计-23级软工.xls"

# 或分步执行
python3 achievement_generator.py "C#程序设计-23级软工.xls"
python3 scripts/review_document.py "C#程序设计-23级软工-课程目标达成情况分析表.docx"
```

### 单独使用

```bash
# 生成文档
python3 achievement_generator.py <Excel文件>

# 审查文档
python3 scripts/review_document.py <输出文件.docx>
```

---

## 📁 目录结构

```
achievement-qztc/
├── SKILL.md                      # 本文件
├── achievement_generator.py       # 主生成器（Generator模式）
├── scripts/
│   └── review_document.py        # 质量审查（Reviewer模式）v2.0
└── references/
    └── grading-formula.md        # 评分公式（Tool Wrapper）
```

---

## 🔄 Pipeline 工作流

```
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: 生成 (Generator)                                  │
│  python3 achievement_generator.py <Excel>                    │
│       ↓                                                    │
│  ✅ CHECKPOINT 1: 文件生成成功？                             │
│       ↓                                                    │
│  STEP 2: 审查 (Reviewer)                                   │
│  python3 scripts/review_document.py <输出.docx>             │
│       ↓                                                    │
│  ✅ CHECKPOINT 2: 所有检查项通过？                          │
│       ↓                                                     │
│  STEP 3: 交付                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 表格与图表

| 组件 | 说明 | 数据源 |
|------|------|--------|
| **表7** | 汇总表 | 各目标平均达成度 + 实际得分 |
| **表8** | 明细表 | 每学生得分/达成度 + 平均行 |
| **Chart1-4** | 散点图 | 每学生各目标达成度 |
| **Chart5** | 柱状图 | 各目标平均达成度百分比 |
| **分析段落** | 文本 | avg/max/min/pct_80/pct_60 |

---

## 🔧 审查检查项（Reviewer模式）

| 检查项 | 说明 |
|--------|------|
| ✅ text_replacement | 所有占位符已替换 |
| ✅ summary_table | 汇总表数据完整 |
| ✅ detail_table | 明细表正确 |
| ✅ charts | 图表数据合理 |
| ✅ analysis_paragraphs | 分析段落正常 |

---

## 📐 评分公式

```python
# 权重和目标配置均从模板表7动态读取（不再硬编码）
# read_weights_and_config_from_template(doc) →
#   weights: 表7 Row 2 的 col3/col4/col5
#   target_config: 表7 各目标理论满分行 (Row 4/7/10/13) 的 col3/col4/col5
#   total = col3×权重.col3 + col4×权重.col4 + col5×权重.col5

# 达成度 = 目标得分 / 理论满分（total）
```

---

## ⚠️ 重要笔记

### 表8平均行结构
```
序号 | 学号 | 姓名 | 目标1得分 | 目标1达成值 | 目标2得分 | 目标2达成值 | ...
平均 | 平均 | 平均 | 得分平均  | 达成度平均  | 得分平均  | 达成度平均  | ...
```

### 图表数据
- Chart1-4: 每学生达成度（0-1范围）
- Chart5: 各目标平均达成度百分比（0-100范围）

---

## 📦 依赖

```python
import pandas as pd
from docx import Document
import zipfile
from lxml import etree
```

---

## 🔄 更新日志

| 版本 | 日期 | 内容 |
|------|------|------|
| **v5.0** | 2026-03-28 | **Pipeline一键执行 + Reviewer v2.0 + references/** |
| v4.4 | 2026-03-28 | 修复表8平均行、Chart5、Charts1-4数据 |
| v4.3 | 2026-03-28 | 表7实际得分 + chart5 |
| v4.0 | 2026-03-27 | 动态表格查找、CLI |

---

*v5.2 - 2026-04-09 - 权重和目标配置从模板表7动态读取*
*v5.0 - 2026-03-28 - Generator + Reviewer + Pipeline*
