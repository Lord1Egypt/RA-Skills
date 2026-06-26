---
name: conversion-path-optimizer-claw
description: |
  转化路径优化虾 — 分析销售漏斗、挖掘高转化话术、给出优化建议的销售智能参谋。

  **当以下情况时使用此 Skill**：
  (1) 需要分析销售漏斗各阶段转化率，找出流失卡点
  (2) 需要从历史 CRM 数据或对话记录中提取高转化话术
  (3) 需要对比不同时间段或不同销售团队的漏斗表现
  (4) 需要根据客户画像（行业、规模、痛点）推荐个性化话术
  (5) 需要设计 A/B 测试方案，量化话术效果
  (6) 需要生成话术手册，培训新人销售
  (7) 用户提到"转化率优化"、"销售话术"、"漏斗分析"、"成交路径"、"话术建议"、"转化提升"、"销售培训"、"客户流失"、"A/B测试"、"销售数据分析"
---

# 转化路径优化虾

分析获客漏斗，挖掘高转化话术，帮助销售团队复制成功经验。

## 工作流程

```
[输入数据] → [数据清洗] → [漏斗建模] → [话术挖掘] → [效果评估] → [推荐输出]
```

## 输入数据格式

**推荐字段（CSV/Excel）**：

| 字段 | 说明 | 必填 |
|------|------|------|
| 客户ID / customer_id | 客户唯一标识 | 是 |
| 阶段 / stage | lead/qualification/demo/negotiation/closed_won/closed_lost | 是 |
| 话术内容 / script | 销售说的话 | 话术分析时必填 |
| 客户反馈 / feedback | 客户回应 | 可选 |
| 最终结果 / result | 成交/流失 | 话术分析时必填 |
| 日期 / date | 沟通时间 | 时间段分析时必填 |

**自然语言输入**：也可直接描述问题，如"最近转化率下降了，帮我分析原因"。

## 使用脚本

### 漏斗分析

```bash
# 分析最近 30 天漏斗（对比 SaaS 行业基准）
python scripts/analyze-funnel.py analyze --input data.csv --days 30 --industry SaaS

# 对比两个月份
python scripts/analyze-funnel.py compare --input data.csv --period1 2026-03 --period2 2026-02

# 导出 HTML 报告
python scripts/analyze-funnel.py export --input data.csv --format html --output report.html
```

### 话术提取

```bash
# 提取 Top 10 高频成交话术
python scripts/extract-scripts.py extract --input data.csv --top 10

# 按转化率排序话术
python scripts/extract-scripts.py rank --input data.csv

# 推荐价格异议话术
python scripts/extract-scripts.py recommend --input data.csv --scenario price_objection
# 可用场景: price_objection | competitor | delay | demo | closing
```

**依赖**：`pip install pandas openpyxl`

## 参考资料

根据任务按需读取：

- **漏斗建模、转化率基准、流失预警** → `references/funnel-modeling.md`
- **话术挖掘算法、对话结构分析** → `references/script-mining.md`
- **A/B 测试设计、话术评分模型** → `references/script-evaluation.md`
- **各行业话术模板（SaaS/电商/B2B）** → `references/industry-templates.md`

## 输出格式

根据用户需求选择输出形式：

1. **漏斗分析报告**：各阶段转化率 + 流失卡点 + 优化建议
2. **话术推荐列表**：按场景分类，附转化率数据支撑
3. **话术手册**：结构化 Markdown，可直接用于培训
4. **飞书文档**：调用 `feishu_create_doc` 生成正式文档

## 注意事项

- 建议至少 100 条成交记录才能产生有效统计洞察
- 话术推荐是统计规律，需结合具体客户灵活调整
- 数据中的客户敏感信息（姓名、手机）建议脱敏后再分析
