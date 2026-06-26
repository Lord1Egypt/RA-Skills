# 可执行 GEO 评估流设计稿

## 目标

本轮升级不把仓库做成依赖大量专有接口的全自动 SaaS，而是做成一个 **可运行、可复现、可审计** 的 GEO monitoring toolkit 骨架。它支持三种场景：

第一种是 **自动采集**。当用户具备可调用模型的 API 时，runner 可以批量跑 Query Pool，生成原始回答、元数据和待标注草稿。

第二种是 **半自动采集**。当某些模型无法自动调用时，团队仍可以把人工复制的回答按统一 schema 导入，再继续走统一打分和周报流程。

第三种是 **修复验证**。当团队做完 README 修正、百科修正、渠道投放或对比稿发布后，可以在 T+7 / T+14 重跑同一批 query，对比动作前后指标变化。

## 目录规范

```text
geo-monitor-toolkit/
├── data/
│   ├── query-pools/
│   ├── runs/
│   └── repair-validations/
├── rubrics/
├── schemas/
├── scripts/
├── templates/
└── .github/workflows/
```

## 运行流

```text
query pool + model config
        ↓
run_monitor.py
        ↓
raw_responses.jsonl + score_draft.jsonl + run_manifest.json
        ↓
人工或二审补充 annotation
        ↓
score_run.py
        ↓
summary.json + metrics.csv
        ↓
generate_weekly_report.py
        ↓
weekly_report.md
        ↓
repair validation / regression comparison
```

## 核心脚本职责

| 脚本 | 输入 | 输出 | 作用 |
|---|---|---|---|
| `run_monitor.py` | Query Pool、模型配置、输出目录 | 原始回答、打分草稿、run manifest | 跑采集与初始化 run |
| `score_run.py` | score draft / annotation 文件 | summary、metrics CSV、validation report | 按 rubric 统一打分 |
| `generate_weekly_report.py` | summary.json、模板 | 周报 Markdown | 生成周报草稿 |
| `validate_data.py` | schema + data files | 校验结果 | 供 CI 和本地检查使用 |

## 评分策略

每条 query-model answer 必须有统一 annotation 记录，四个指标全部采用 **0-2 离散分值**，再统一转换为 0-100 指标，避免“看起来像 rate 其实是主观感受”的漂移。

| 指标 | 0 分 | 1 分 | 2 分 |
|---|---|---|---|
| mention_score | 未提及目标产品 | 提及但非主推，或仅并列列举 | 明确主推或第一推荐 |
| sentiment_score | 负面、劝退、错误贬损 | 中性、条件式、无明显倾向 | 正面推荐且给出理由 |
| capability_score | 核心能力描述错误或缺失 | 部分正确，有明显遗漏 | 核心能力正确且边界清晰 |
| ecosystem_score | 生态、SDK、集成关系错误或缺失 | 部分正确，存在遗漏 | 生态关系准确完整 |

## 指标公式

为兼容原有“率”的表达，summary 中统一输出四类 0-100 指标：

- `mention_rate = mean(mention_score / 2) * 100`
- `positive_mention_rate = mean(sentiment_score / 2) * 100`，但仅在 mention_score > 0 的记录中计算
- `capability_accuracy = mean(capability_score / 2) * 100`，仅在 capability 类 query 中计算
- `ecosystem_accuracy = mean(ecosystem_score / 2) * 100`，仅在 ecosystem 类 query 中计算

同时额外输出 `strict_win_rate` 指标，用于统计 2 分记录占比，便于更严格复盘。

## 标注协议

每条记录至少包含以下字段：

| 字段 | 含义 |
|---|---|
| `run_id` | 本次运行唯一标识 |
| `query_id` | Query Pool 中的 query ID |
| `query_type` | brand / capability / ecosystem / competitor / negative |
| `model_id` | 模型标识 |
| `response_text` | 原始回答 |
| `source_links` | 回答中的链接或人工补录链接 |
| `mention_score` | 0-2 |
| `sentiment_score` | 0-2 |
| `capability_score` | 0-2 |
| `ecosystem_score` | 0-2 |
| `needs_repair` | 布尔值 |
| `repair_type` | info_error / negative_eval / outdated / competitor_insertion / none |
| `annotator` | 打分人 |
| `review_status` | draft / reviewed / approved |

## Schema 设计

需要至少提供三类 schema：

1. Query Pool schema：保证每条 query 都有产品、语言、优先级、类型与文本；
2. Run results schema：保证每次 run 的 manifest、原始回答、标注结果和汇总结构一致；
3. Repair validation schema：保证动作、目标 query、验证窗口、前后指标变化可追踪。

## 修复验证设计

修复验证对象不是单篇内容，而是一个结构化实验。

| 字段 | 说明 |
|---|---|
| `action_id` | 修复动作唯一 ID |
| `action_type` | README 修正、百科更新、渠道投放、FAQ 发布等 |
| `target_queries` | 受影响 query 列表 |
| `baseline_run_id` | 修复前 run |
| `followup_run_ids` | T+7 / T+14 run |
| `expected_change` | 预期提升指标 |
| `observed_change` | 实际变化 |
| `conclusion` | success / mixed / failed |

## 样例覆盖策略

为证明泛化能力，本轮新增至少三个不同行业 Query Pool：

| 类型 | 示例项目 |
|---|---|
| SaaS | PostHog |
| Open-source library | FastAPI |
| Developer tool | Langfuse |

这些样例不是为了宣称结论，而是为了展示 **同一套 schema 和 runner 可以适配不同对象**。
