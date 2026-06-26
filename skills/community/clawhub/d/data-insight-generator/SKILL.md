---
name: data-insight-generator
version: 1.0.0
author: AI-Workflows
license: MIT
description: 零代码BI分析器，支持CSV/JSON数据自动清洗、指标计算、图表推荐与业务洞察输出
tags:
  - 数据分析
  - BI
  - 可视化
  - 业务洞察
  - 零代码
parameters:
  data_content:
    type: string
    required: true
    description: CSV/JSON数据片段或字段结构描述（需含表头与示例行）
  business_context:
    type: string
    required: true
    description: 业务场景（销售/库存/用户增长/财务/供应链等）
  analysis_goal:
    type: string
    required: false
    description: 分析目标（如：找出流失原因/优化库存周转/评估活动ROI）
output_format: markdown
compatibility:
  - OpenClaw
  - Dify
  - Coze
  - SkillHub
---
# 📊 零代码BI分析器

## 🎯 核心定位
让业务人员通过自然语言完成“数据探查→指标计算→图表推荐→结论输出”全链路，替代 30% 轻量级 BI 需求。

## 🔄 工作流指令
1. **结构解析**：识别 `data_content` 中的字段类型（数值/分类/时间/文本），标记缺失值、异常值与重复项。
2. **指标计算**：结合 `business_context` 与 `analysis_goal`，推导核心业务指标（同比/环比/转化率/漏斗/帕累托/留存等）。
3. **图表匹配**：按数据维度自动推荐最佳可视化方案（折线/柱状/散点/热力/桑基/漏斗），输出配置伪代码。
4. **洞察提炼**：生成 3 条可执行业务建议，严格区分“相关性”与“因果性”，附加数据局限性声明。
5. **模板输出**：按标准 Markdown 结构生成报告。

## 📤 输出模板
```markdown
# 📈 数据分析与洞察报告

## 1. 数据质量摘要
| 指标 | 值 | 备注 |
|:---|:---|:---|
| 总记录数 | ... | ... |
| 缺失/异常字段 | ... | 建议补全/清洗策略 |
| 时间跨度/粒度 | ... | ... |

## 2. 核心指标看板
| 指标名称 | 计算逻辑 | 当前值 | 趋势 | 业务含义 |
|:---|:---|:---|:---|:---|
| ... | ... | ... | ↑/↓/→ | ... |

## 3. 图表推荐配置
- **图表类型**：...
- **X/Y轴映射**：...
- **可视化代码片段**：`[ECharts Option / Python Snippet]`

## 4. 业务洞察与行动建议
1. 发现：... → 建议：...
2. 发现：... → 建议：...
> ⚠️ 分析基于当前数据切片，未包含未采集维度。重大决策请结合实地调研与业务校验。
