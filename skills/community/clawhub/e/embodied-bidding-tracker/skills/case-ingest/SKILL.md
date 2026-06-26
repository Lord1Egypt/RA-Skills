---
name: airs-case-ingest
description: >
  生成具身智能案例最终入库表的 AIRS 研究 Skill。用于读取人工复核后的 data/output/ingestion_output.csv，执行去重、字段修正、企业简称映射、人工覆写、LLM 案例详情质检和案例简介生成，输出 data/output/ingest_final.csv 与 ingest_report.md。用户需要生成最终数据库入库文件、处理新增通过记录或做增量 ingest 时使用。
  Keywords: AIRS, 具身智能, embodied intelligence, case ingest, database ingestion, 入库表, 案例库, 去重, 数据质检, 案例简介, robot case database, knowledge asset.
tags: ["airs", "AIRS", "具身智能", "embodied-intelligence", "case-ingest", "database", "data-quality", "deduplication", "案例库", "入库", "knowledge-asset"]
---

# 标准入库表生成

## 目标

将人工确认通过的候选案例转成最终入库格式，对照既有数据库去重，并统一企业简称、金额、型号、案例详情和案例简介。

## 输入

- `data/output/ingestion_output.csv`
- 既有数据库 Excel，例如 `具身智能案例入库_2026Q1_0313核实版v2.xlsx`
- `data/company_list.csv`
- `src/ingest_verify.js` 中的人工覆写规则
- `config/settings.json` 中的 OpenAI-compatible LLM 配置与本地 API key

## 输出

- `data/output/ingest_final.csv`
- `data/output/ingest_report.md`
- `data/ingest_progress.json`

增量处理中间输出：

- `data/output/ingestion_output_delta.csv`
- `data/output/ingest_final_delta.csv`
- `data/output/ingest_report_delta.md`

## 执行流程

全量入库：

```bash
npm run ingest
```

只处理新增通过记录时，可先生成差集输入，再调用脚本参数：

```bash
node src/ingest_verify.js --input data/output/ingestion_output_delta.csv --output data/output/ingest_final_delta.csv --report data/output/ingest_report_delta.md --progress data/ingest_progress_delta.json
```

结束后查看：

1. `data/output/ingest_final.csv` 是否为最终全量入库文件。
2. `data/output/ingest_report.md` 中的跳过、修正、覆写和 warning。
3. 场景枚举 warning、金额异常、企业简称未映射问题。

## 业务规则

- Ingest 去重键：`(机器人企业, 场景需求方, 部署季度)`。
- 机器人企业优先映射为 `company_list.csv` 中的企业简称。
- 金额非数字填 `-`。
- 机器人型号为空、未披露或无效时填 `-`。
- 父记录为空填 `-`。
- 案例详情和案例简介写出前压成单行，避免 CSV 单元格内换行。
- 案例详情标准：150-250 字；案例简介标准：30-60 字。
- `ingest_final_delta.csv` 只是增量中间结果，不是最终入库文件。

## 人工覆写

- 高频修正可先写入 `src/ingest_verify.js` 的 `MANUAL_OVERWRITES`。
- 覆写应记录原因，避免同一条记录在后续批次反复被 LLM 改回。
- 后续可迁移到 `config/manual_overwrites.json`，方便非工程人员维护。

## 失败处理

- LLM 质检失败：保留 progress 直接重跑。
- 既有数据库路径变化：使用 `--input/--output/--report/--progress` 参数明确指定。
- 最终表记录少于预期：回查 `review_sheet.csv` 的 `人工决定` 和 `ingestion_output.csv`。
