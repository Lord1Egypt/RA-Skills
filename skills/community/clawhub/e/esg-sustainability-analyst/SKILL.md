---
name: ESG Sustainability Analyst
slug: esg-sustainability-analyst
description: 企业ESG报告生成与可持续发展评估技能。覆盖GRI/ISSB/SASB多标准框架，自动收集碳排放数据、生成合规报告，并提供减排路径建议。适用场景：企业ESG披露、投资者尽调、碳中和规划。
version: 1.0.0
author: ai-gaoqian
tags:
  - esg
  - sustainability
  - carbon-accounting
  - compliance
  - reporting
metadata:
  openclaw:
    requires:
      - web_search
      - data_analysis
---

# ESG Sustainability Analyst

## 核心能力

| 能力模块 | 功能描述 |
|---------|---------|
| 碳排放核算 | 基于GHG Protocol的Scope 1/2/3排放自动计算，支持多行业排放因子库 |
| ESG报告生成 | 一键生成符合GRI/ISSB/SASB/TCFD标准的ESG报告，包含数据可视化 |
| 合规检查 | 对标EU CSRD、SEC气候披露规则、中国ESG指引，发现差距并给出补齐建议 |
| 减排路径建议 | 基于行业基准的减排场景分析，推荐SBTi科学碳目标路径 |
| 供应链ESG评估 | 供应商ESG风险评分，支持Tier 1-3穿透分析 |

## 触发场景

- 企业准备年度ESG报告
- 投资者对被投企业进行ESG尽调
- 碳交易与碳中和规划
- 供应链可持续发展评估
- 评级机构（MSCI/Sustainalytics/CDP）评分提升

## 执行流程

1. **数据收集**：引导用户提供能耗、差旅、废弃物等关键数据，缺失项通过行业基准估算
2. **核算阶段**：按GHG Protocol分类计算碳排放，输出可审计的核算底稿
3. **报告生成**：根据用户指定框架生成结构化ESG报告，含KPI仪表板
4. **差距分析**：对标最新法规要求，标注高风险领域和合规时间线
5. **改进建议**：输出优先级排序的改进行动清单，含预期减排量和成本估算

## 输出格式

- ESG报告正文（Markdown/PDF）
- 碳排放核算底稿（CSV/Excel）
- KPI仪表板（表格式数据）
- 合规差距矩阵（表格）
- 改进路线图（时间轴+行动项）

## 注意事项

- 核算结果依赖用户提供数据质量，缺失数据使用行业均值并标注
- 不构成法律或审计意见，重大决策需咨询专业人士
- 排放因子库定期更新，建议每次使用时确认版本号
- 支持中英文双语输出
