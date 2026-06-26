---
name: 保险Excel自动数据分析工具
description: |
  保险Excel自动数据分析工具，是基于保险从业人员常用的excel数据字段进行筛选和分析的AI自动数据分析skills。
  触发词：数据分析、分析数据、生成图表、制作图表、数据报告、EDA、探索性分析、可视化分析、统计报告。
  当用户提供数据文件并要求分析、生成图表、制作报告时，自动触发本 Skill。
metadata:
  version: "1.0.1"
  author: "WuWenBin-BeiJing-ST"
  license: "MIT"
---

# 保险Excel自动数据分析工具 V1.0.1

> **作者**: WuWenBin-BeiJing-ST
>
> 2026 年，保险行业的数据分析涉及到数据清洗和数据整理，这些工作应该交给 Skills 自动完成。本 Skill 专为保险从业人员设计，针对保险Excel数据字段进行智能分析，从原始数据到专业报告，一键搞定。

## 前言

保险行业的数据分析涉及到数据清洗和数据整理，2026 年，这些基础工作应该交给 Skills。本 Skill 专为保险从业人员设计，能够自动识别保险常用字段（如保单号、险种、保费、理赔金额、客户信息等），自动制作图表（柱状图、饼状图、带数据标记的折线图、条形图），数据分析能力具备：

1. **标准数据分析流程**（EDA → 清洗 → 分析 → 可视化 → 洞察 → 输出）执行，同时处理常见文件格式（CSV、Excel、JSON）
2. Agent 在 Skill 里自动调用 Kimi/DeepSeek 生成自然语言洞察部分
3. 具备导出 Word 报告的能力

## 能力概览

本 Skill 提供端到端数据分析能力，涵盖从原始数据到专业报告的完整流程：

1. **数据加载** — 支持 CSV、Excel (.xlsx/.xls)、JSON 格式，自动识别编码
2. **EDA 探索** — 数据概览、缺失值分析、类型推断、描述性统计
3. **数据清洗** — 删除空行/重复行、缺失值填充、异常值标记
4. **统计分析** — 数值列统计、分类列频次、相关性分析
5. **可视化** — 自动生成柱状图、饼状图、折线图、条形图（PNG 格式）
6. **AI 洞察** — 调用 Kimi/DeepSeek 生成自然语言业务洞察
7. **报告导出** — 一键生成专业 Word 分析报告

## 快速开始

```bash
# Step 1: 执行数据分析（EDA + 清洗 + 统计 + 图表）
python3 scripts/analyze.py <数据文件路径> --output-dir ./output

# Step 2: 生成 Word 报告（洞察文本由 Agent 调用 Kimi/DeepSeek 生成）
python3 scripts/export_report.py ./output/summary.json "<AI洞察文本>" --output ./报告.docx
```

## 标准工作流

```
用户上传数据文件
       ↓
[1] 加载数据（CSV/Excel/JSON）
       ↓
[2] EDA 探索性分析
       ↓
[3] 数据清洗（自动 + 日志记录）
       ↓
[4] 统计分析（数值 + 分类）
       ↓
[5] 可视化（自动生成四类图表）
       ↓
[6] AI 洞察生成（调用 Kimi/DeepSeek）
       ↓
[7] 导出 Word 报告
       ↓
返回报告文件给用户
```

详细流程说明见 [references/workflow.md](references/workflow.md)。

## 脚本说明

### `scripts/analyze.py`

**功能**: 数据分析核心脚本，执行 EDA、清洗、统计、图表生成。

**用法**:
```bash
python3 scripts/analyze.py <数据文件> [--output-dir <输出目录>]
```

**输出**:
- `summary.json` — 完整分析结果（EDA、清洗日志、统计、图表路径）
- `charts/*.png` — 自动生成的可视化图表

**依赖**: pandas, matplotlib, numpy, openpyxl

### `scripts/export_report.py`

**功能**: 生成 Word 格式数据分析报告。

**用法**:
```bash
python3 scripts/export_report.py <summary.json路径> "<洞察文本>" [--output <报告路径>]
```

**输出**: 专业排版的 Word 文档，包含封面、数据概览、清洗记录、统计分析、图表、AI 洞察、结论建议。

**依赖**: python-docx

## AI 洞察生成

本 Skill 需 Agent 调用外部大模型（Kimi 或 DeepSeek）生成自然语言洞察。

详细调用方式、Prompt 模板、环境变量配置见 [references/insight_generation.md](references/insight_generation.md)。

**关键配置**:
```bash
# Kimi API Key
export KIMI_API_KEY="your-kimi-api-key"

# DeepSeek API Key
export DEEPSEEK_API_KEY="your-deepseek-api-key"
```

## 图表类型

| 图表类型 | 适用场景 | 自动生成条件 |
|---------|---------|-------------|
| 柱状图 | 数值分布、分类频次 | 数值列最多 3，分类列最多 2 |
| 饼状图 | 分类占比 | 分类列唯一值 ≥ 2，最多 2 列 |
| 折线图 | 数值趋势（带数据标记） | 数值列数据点 ≥ 2，最多 3 列 |
| 条形图 | 分类排名（水平） | 分类列唯一值 ≥ 2，最多 2 列 |

所有图表自动适配中文字体（PingFang SC / SimHei / Microsoft YaHei 等）。

## 支持的数据格式

| 格式 | 扩展名 | 编码处理 |
|------|--------|---------|
| CSV | .csv | 自动尝试 utf-8 / utf-8-sig / gbk |
| Excel | .xlsx, .xls | 自动读取，支持多 Sheet（默认第一个） |
| JSON | .json | 支持数组格式、对象数组、键值对映射 |

## Agent 执行指南

当用户触发本 Skill 时，按以下步骤执行：

1. **确认数据文件路径** — 用户上传或指定路径
2. **执行 analyze.py** — 生成 `summary.json` 和图表
3. **读取 summary.json** — 提取关键信息构建 Prompt
4. **调用 Kimi/DeepSeek** — 生成自然语言洞察
5. **执行 export_report.py** — 生成 Word 报告
6. **返回报告文件** — 提供下载路径或直接发送给用户

**错误处理**:
- 缺少依赖 → 提示用户运行 `pip3 install pandas matplotlib numpy openpyxl python-docx`
- 缺少 API Key → 提示配置环境变量
- 数据格式错误 → 提示用户检查文件格式

## 参考文档

- [工作流详解](references/workflow.md) — 标准流程、判断逻辑、常见问题
- [洞察生成指南](references/insight_generation.md) — Kimi/DeepSeek 调用方式、Prompt 模板
