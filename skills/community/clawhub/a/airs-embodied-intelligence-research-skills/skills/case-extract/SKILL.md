---
name: airs-case-extract
description: >
  从天眼查招投标公告原文中提取具身智能应用案例的 AIRS 研究 Skill。用于读取 data/bidding_records.csv 与 data/raw_content/*.md，调用 LLM 提取准入结果、场景分类、需求方、机器人型号、金额、部署时间和案例详情，生成 extract_results.csv、review_sheet.csv 与 ingestion_output.csv。用户需要把公告证据转成候选入库案例或刷新人工复核表时使用。
  Keywords: AIRS, 具身智能, embodied intelligence, case extraction, LLM extraction, 招投标案例, 应用案例, 场景分类, structured data, robot deployment, research workflow.
tags: ["airs", "AIRS", "具身智能", "embodied-intelligence", "case-extraction", "LLM", "structured-data", "scenario-classification", "机器人案例", "招投标案例", "research-workflow"]
---

# 招投标案例提取

## 目标

从公告原文中提取结构化案例字段，判断是否符合具身智能应用案例入库标准，并生成人工复核表。

## 输入

- `data/bidding_records.csv`
- `data/raw_content/*.md`
- `应用场景分类规则.md`
- `config/settings.json`
- `config/settings.json` 中的 OpenAI-compatible LLM 配置与本地 API key

## 输出

- `data/extract_results.csv`
- `data/review_sheet.csv`
- `data/output/ingestion_output.csv`
- `data/extract_progress.json`

## 执行流程

1. 确认 `data/raw_content/*.md` 存在且非空。
2. 运行：

```bash
npm run extract
```

3. 在 `data/review_sheet.csv` 中人工确认 `待验证` 行。
4. 将应入库记录的 `人工决定` 改为 `通过`。
5. 重跑：

```bash
npm run extract
```

6. 使用刷新后的 `data/output/ingestion_output.csv` 进入标准入库技能。

## 字段规则

- `admissionResult`：通过 / 不通过 / 待验证。
- 一级、二级场景必须来自 `应用场景分类规则.md`。
- 金额统一为万元纯数字；未披露填 `-`。
- 机器人型号为空或未披露时填 `-`。
- 案例详情 150-250 字，突出真实任务、部署规模、可量化指标和里程碑；不要写“未披露/暂无”等负面占位。
- Extract 去重键：`(robotCompany, demandSide, deployQuarter)`，保留首条。

## 人工复核重点

- `准入结果=待验证` 的记录。
- 场景分类不确定或二级场景不在枚举中的记录。
- 需求方、机器人企业、型号、金额明显来自表头或错误段落的记录。
- 案例详情出现营销语、公司介绍、行业背景而非部署事实的记录。

## 失败处理

- LLM Key 缺失：在本地 `config/settings.json` 中填写 `openaiCompatible.apiKey`。
- 原文缺失：先运行 `npm run crawl:rawcontent`。
- 断点续跑：保留 `data/extract_progress.json`，直接重跑命令。
