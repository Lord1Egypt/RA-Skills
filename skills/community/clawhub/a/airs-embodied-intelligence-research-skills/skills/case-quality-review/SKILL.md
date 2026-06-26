---
name: airs-case-quality-review
description: >
  复查具身智能案例质量的 AIRS 研究 Skill。用于对已提取或已入库候选案例执行质量回检，重点检查场景枚举、案例详情可信度、案例简介一致性、企业简称映射、金额和型号规范，产出 ingest_report.md 中的 warning、修正和覆写记录。用户需要回检已沉淀案例、处理质量 warning、复查案例详情或发布前做最终质量审核时使用。
  Keywords: AIRS, 具身智能, embodied intelligence, quality review, case review, 数据质检, 案例复查, warning, 场景枚举, 案例详情, robot case quality, final QA.
tags: ["airs", "AIRS", "具身智能", "embodied-intelligence", "quality-review", "case-review", "data-quality", "QA", "案例复查", "质量审核", "warning"]
---

# 案例质量复查

## 目标

对已进入入库链路的具身智能案例做质量回检，确认案例事实、场景分类、主体简称、案例详情和案例简介可以支撑发布或入库。

## 输入

- `data/output/ingestion_output.csv`
- `data/company_list.csv`
- `应用场景分类规则.md`
- `src/ingest_verify.js` 中的人工覆写规则
- `config/settings.json` 中的 OpenAI-compatible LLM 配置与本地 API key

## 输出

- `data/output/ingest_final.csv`
- `data/output/ingest_report.md`
- `data/ingest_progress.json`

## 执行流程

运行质量复查：

```bash
npm run quality:review
```

复查结束后：

1. 阅读 `data/output/ingest_report.md`，重点查看 warning、字段修正、人工覆写和跳过记录。
2. 抽查 `data/output/ingest_final.csv` 中的案例详情和案例简介，确认没有负面占位、空泛营销语或事实外推。
3. 对反复出现的主体、型号、金额或详情错误，优先写入 `src/ingest_verify.js` 的 `MANUAL_OVERWRITES`。
4. 修正后重跑本技能，直到报告中的关键 warning 可解释或已处理。

## 复查重点

- 一级、二级场景是否来自 `应用场景分类规则.md`。
- 机器人企业是否已映射为 `company_list.csv` 中的简称。
- 金额是否为万元数字，未披露时是否为 `-`。
- 机器人型号为空、未披露或无效时是否为 `-`。
- 案例详情是否围绕真实项目事实，不写“未披露/暂无”等负面占位。
- 案例简介是否能在 30-60 字内概括真实部署事实。

## 失败处理

- LLM 质检失败：保留 progress 后重跑。
- 记录数少于预期：回查 `review_sheet.csv` 的 `人工决定` 和 `ingestion_output.csv`。
- warning 无法自动修正：记录为人工复核项，不要强行改写事实。
