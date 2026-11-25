# Query control · 问数控制单（0.3.4）

Use this after a question selects a metric. Business users describe the question and review meanings; the host Agent/FDE proposes bindings through the existing candidate/edit workflow. Do not ask users to write JSON or confirm invented defaults. This is a reviewed handoff contract, **not a SQL compiler, query gateway or authorization grant**.

## Read a delivered question

```bash
python -X utf8 scripts/semantic_read.py --package ./delivery/question.zip verify
python -X utf8 scripts/semantic_read.py --package ./delivery/question.zip control
python -X utf8 scripts/semantic_read.py --package ./delivery/question.zip task --detail summary
python -X utf8 scripts/semantic_read.py --package ./delivery/question.zip sources --id METRIC_ID
```

`control` returns the entire declared dependency closure, selected columns, declared aggregation/filters/time scope, evidence gaps and blockers. It reads all context pages internally. `task`/`context` still paginate: consume their remaining pages when needed. Exit code 0 means successful reading, including a blocked decision; it never means execute the query.

| Decision / state | Meaning |
| --- | --- |
| `explain_only` | Explanation was requested. Read gaps and evidence; it is not an assertion that the answer is complete. |
| `blocked` | Query/calculation/action cannot be authorized by this offline package. Resolve semantic blockers before any separate runtime integration. |
| `plan_status: declared` | A structurally supported plan is present, with no identified semantic blocker. **No machine proof** of prose-to-plan equivalence, question coverage or runtime correctness. |
| `plan_status: incomplete` | Missing, ambiguous, changed or unsupported binding; inspect blockers. |

0.3.4 never emits `executable`. A text `executor_id`, URL, instruction or a passing example cannot establish runtime identity, tenant authorization, row policy, current catalog, resource limits or an execution receipt. An independently authorized runtime remains responsible for those checks and actual results. Legacy numeric tools are separate and do not become query-control executors.

## One canonical definition

Keep bindings on `document.model.semantic.assets[].properties.query_plan`, **only on a metric**. They go through the same revision, candidate review, audit and impact checks as other properties. `query_control.json` is derived; never hand-edit it as another source of truth.

The supported declaration is deliberately narrow: one dataset, scalar filters and one aggregation. A host proposes this shape using actual discovered IDs:

```json
{
  "dataset_id": "actual.dataset.id",
  "column_ids": ["actual.field.id", "actual.field.lab", "actual.field.disabled"],
  "grain_ids": ["actual.field.lab"],
  "relation_ids": [],
  "mapping_ids": ["actual.business.mapping"],
  "rule_ids": ["actual.scope.rule"],
  "aggregation": {"function": "count_distinct", "field_id": "actual.field.id"},
  "filters": [{"field_id": "actual.field.disabled", "op": "eq", "value": 0}],
  "null_policy": "exclude",
  "time_scope": "the reviewed metric time scope",
  "semantic_fingerprint": "computed after reviewing the metric meaning"
}
```

This is a schema illustration, not a complete equipment query. Do not copy these placeholder IDs or infer the omitted Lab filter. The included equipment exercise supplies a complete authored declaration for its own source material, including Lab L, in-store state and disabled=0, then requires normal review.

Contract:

- `column_ids` explicitly lists fields belonging to the selected dataset through field `refs`. Each field has a physical `properties.column` and a value type. Do not bind by name similarity.
- `grain_ids` identifies the business grouping level; it is **not necessarily a primary key**. The aggregation operand independently specifies what is counted or summed.
- `mapping_ids` references confirmed mappings to that dataset. It does not prove the transformation correct. Explicit `strength: weak` remains blocked.
- `relation_ids` contains only relations needed for the question. No relation is required for a single-table filter. Selected cross-table relations are delivered for review, but return `PATH_NOT_EXECUTION_VALIDATED`; this release does not validate join keys, time alignment or fanout and never generates joins.
- `rule_ids` references applicable scope and prohibition rules. Omission is not evidence that no other rules exist: question coverage remains unverified.
- Aggregations: `count_distinct/count/sum/min/max`; scalar operators: `eq/ne/gt/gte/lt/lte/is_null/not_null`. The declaration preserves 0, false and NULL distinctly. NULL comparisons use explicit null operators. Unsupported expressions remain blockers; never silently translate them into a supported approximation.
- `null_policy` declares `exclude` or `preserve`; review its intended effect together with the aggregation and filter semantics. It is not implemented SQL behavior. More nuanced per-field policies require a future contract version.
- `time_scope` must equal the reviewed metric's text. It describes data time and remains subject to interpretation/implementation review. `task.as_of` instead checks definition validity; neither proves data freshness.
- `semantic_fingerprint` is computed by `workbench.query_control.semantic_fingerprint(metric)` after alignment review. It hashes definition, scope and non-plan properties to detect later changes; computing it does not prove that review occurred. Do not refresh it solely to clear a warning.

All declared field, mapping, rule and relation references join the common dependency closure, context edges and question impact analysis. A field rename must make affected observations stale; unrelated columns stay outside the scoped package. Existing projects without bindings remain readable and return `NO_PLAN`; the host must propose real dependencies, not silently rewrite confirmed history.

## Snapshot and compatibility

Question handoff uses `semantic-package/1.1`: the existing five files plus `task.json` and `query_control.json`. Knowledge-only exports remain `semantic-package/1.0`. The 0.3.4 reader accepts old packages; `control` returns `NO_CONTROL` for them. Older readers reject the new format rather than silently ignoring its control.

The control binds snapshot, model hash and task hash; the manifest hashes the control file. The reader recomputes the control from canonical inputs, rejecting tampered decisions even if file hashes were rewritten. These checks prove internal consistency, **not source authenticity or trust**. The control's own hash excludes its `control_sha256` and the reader-added `status` field.

`control --scenario ID` rejects a different task. `--expected-snapshot ID` detects a mismatch with a caller-supplied reference (`STALE_SNAPSHOT`), retaining `stored_control_sha256` and computing a new response control hash. A match is not proof that the reference is current. Offline freshness stays `unknown_offline`; copies cannot revoke themselves.

`SOURCE_REVISION_AHEAD` means a newer source revision was already registered **at export**, while a definition still cites an older revision. The package preserves that fact without copying unrelated source text, judging the new rule or rewriting historical definitions. Review applicability in the authoring project; a historical interpretation can legitimately retain the older citation. It does not detect changes after export.

## 工作台与接收方怎么配合

在“业务问题”保存并检查，展开“问数交付边界”即可查看字段、过滤、时间和所选关系。已有本合同支持的绑定时，点击“核对指标与绑定”可按字段名称调整聚合、粒度、AND 过滤、空值和时间，并在同一界面核对原文。数字、文字、布尔与空值分别输入；不支持的条件不能自动改成近似条件。修改时间会同步原指标的 time_scope，定义正文仍须人工核对。

保存必须记录核对依据，经原 `edit` 事务、修订与影响路径更新同一个指标；仅在明确确认 `review_query_plan` 且提供 `plan_review_reason` 时，由服务重算 semantic_fingerprint 并保存人工依据。这是显式人工核对记录，不是机器证明文字和计划等价。普通资产编辑不自动刷新这个指纹。

缺绑定或包含本表单不支持的表达式时，保留内容并让宿主按已有材料提出候选。数据集、映射和关系的变更仍回到原模型核对；本表单不是通用查询编排器。

生成问题包后，问题编辑或当前项目修订变化会撤下本页旧下载入口，防止把历史包误认成当前内容。已发出的文件保持不变。新来源的未知影响、未验证的答案、没有运行时授权分别保留，不以“保存成功”或“包完整”掩盖。

接收方先读 `control`，再按需读 `task`、具体定义及 `sources`。本版能缩短定位缺项的过程，但没有用户研究证明“零门槛”，也没有生产执行、准确率或性能承诺。
