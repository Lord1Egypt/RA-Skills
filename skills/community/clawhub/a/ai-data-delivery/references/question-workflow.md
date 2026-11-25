# Business questions → reviewed semantics → Agent context

业务问题 → 核对含义 → Agent 上下文。This is the host/operator path added in v0.3.1-dev. It uses the existing source, candidate, graph and publication services; it adds no model API, second ontology or production executor.

## Start with a real question / 从真实问题开始

In **Business questions / 业务问题**, record what the user wants to explain, calculate, retrieve or do. Keep a business-provided expected example or exception when one is available. Do not require an expectation before saving an exploratory question, and do not invent one from the generated graph.

The following equipment scenario illustrates the question format. The optional fixture is in the [source repository](https://github.com/franklinxkk/ai-data-delivery/tree/v0.3.6/examples), and the installed quick start uses transport instead.

- Question: “How many items are available to borrow in Lab L?” / “实验室 L 有多少台可借设备？”
- Intent: `query` — the user wants records or a current count; choosing this intent does not enable execution.
- Independent expectation from the supplied material: Lab L only, in storage, not disabled, distinct equipment IDs; without inventory observations, no current count can be reported. Other labs and disabled equipment are counterexamples.

The scenario holds the question, selected asset IDs, optional filters/date and notes. Optional declared context criteria are checked; example observations remain unverified until explicitly recorded. See [acceptance, impact and handoff](question-delivery.md). Definitions remain in `document.model.semantic.assets`; scenarios remain task metadata in `document.knowledge.scenarios`. Saving a question does not confirm, edit or publish any semantic asset. Reopening a v0.3.0 project does not insert fictional scenarios or rewrite existing semantics.

场景中的“预期样例／例外”是人工预期，检查不会把它自动判为通过。需要真实数据验证时另走已授权执行环境，不能用生成模型反过来生成一个必然通过的答案。

## Reuse before adding / 先复用再补充

Search existing definitions by names, aliases, domain and scope. A question with no selected roots can return lexical candidate suggestions; names and token overlap are discovery hints, not a semantic understanding claim. Choose stable IDs from actual evidence. No IDs are selected automatically, even when only one candidate matches. The host can resolve obvious existing definitions; ask the operator about material ambiguities rather than forwarding every technical selection.

Scopes and dates constrain applicability. A scope string is an exact value, and a structured scope filter matches an object subset; inspect actual stored values instead of inventing a shorthand. A selected root that does not match explicit filters is rejected. Required dependencies still accompany selected roots, even if their own domain/scope labels differ. Filters must not remove a restriction the selected definition requires. These are semantic filters, not tenant authorization.

Choose only meanings needed for this question, but retain their restrictions and dependencies. The full graph remains available for expert editing. If a concept already has a confirmed definition, reuse it. A conflicting meaning may require a distinct identity or a proposed change; a similar name alone does not decide which.

## Host commands

These are **host-maintained** files and commands. Ordinary users should not be asked to write JSON or learn IDs. Run from the installed skill directory. Substitute actual project paths, revisions, IDs and operation UUIDs.

Read current state, then save a question:

```bash
python -X utf8 scripts/knowledge.py --project "./work/equipment" state
python -X utf8 scripts/knowledge.py --project "./work/equipment" --revision PROJECT_REVISION --operation-id OPERATION_ID scenario --file "./work/question.json"
```

Example `question.json`, **only for an initialized equipment exercise whose definitions have been reviewed**:

```json
{
  "title": "Available equipment",
  "question": "How many items are available to borrow in Lab L?",
  "intent": "query",
  "asset_ids": ["demo.available"],
  "acceptance_notes": "Lab L only; in storage and not disabled; distinct equipment IDs. Other labs are excluded. No current count without inventory observations."
}
```

Use `asset_ids: []` when relevant definitions have not yet been selected. Other optional fields are `domain`, `scope` (string or object), and `as_of` (definition-applicability date `YYYY-MM-DD`). `as_of` checks the validity intervals of the selected definitions and their dependencies; missing bounds remain unknown. A data cutoff or latest-record rule belongs in the reviewed metric's `properties.time_scope` and evidence, not this filter. Leave `as_of` unspecified unless definition applicability is being requested; do not invent validity dates to clear a check. / `as_of` 是定义适用日期，取数截点写入指标时间范围及依据；未提供的定义有效期不能自动补齐。

Use the returned `id` for later updates. Updating a scenario preserves omitted fields; explicitly change a field only when intended. Question metadata is not provenance for a new business assertion.

Readiness is a read operation on the current saved question:

```bash
python -X utf8 scripts/knowledge.py --project "./work/equipment" check --scenario SCENARIO_ID
```

The result identifies the scenario and revision, contains the reader result, and states `answer_verified: false`, `published: false` and a separate `acceptance` report (initially `not_verified`). A check does not run SQL, call an LLM, execute business actions or create a snapshot. A later project revision requires a fresh check; an earlier result is not current evidence.

When meaning is missing, import authorized materials through the existing path and prepare the matching batch with the saved question:

```bash
python -X utf8 scripts/knowledge.py --project "./work/equipment" --language en import --file "./materials/policy.txt"
python -X utf8 scripts/knowledge.py --project "./work/equipment" --language en task --batch BATCH_ID --scenario SCENARIO_ID
```

`task` is a state-changing preparation step, not an LLM call. Read its returned materials, current assets, question and previous candidate dispositions. Interpret the sources in the host, prepare full evidence-linked candidates using the [candidate contract](m1-m2-contract.md), then submit them:

```bash
python -X utf8 scripts/knowledge.py --project "./work/equipment" --revision PROJECT_REVISION --operation-id OPERATION_ID propose --batch BATCH_ID --file "./work/candidates.json"
python -X utf8 scripts/knowledge.py --project "./work/equipment" receipt OPERATION_ID
```

Continue this handoff directly when the current host has authorized tool access. The UI's **Prepare host task for this question / 准备当前问题的 Agent 任务** offers copyable instructions for environments where the host is not connected; it is a fallback, not a required manual step in every turn. No embedded model is invoked by that button.

Use `--partial` for an incomplete proposal batch. On uncertain writes, query the original receipt before retrying and reuse an operation ID only with identical payload. On revision conflicts, inspect current changes and preserve inputs instead of blindly resubmitting. Cancelled tasks reject late proposals; explicitly resume and inspect existing groups before continuing. No host retry may erase a rejection or manual correction.

## Review the decision / 核对真正影响结果的决定

Candidate group summaries should make these points visible in business language:

| Review content | Example |
| --- | --- |
| Meaning being proposed | Available equipment excludes disabled equipment. |
| Evidence | The exact policy paragraph and source revision. |
| Effect on the question | A disabled item in Lab L must not count as available. |
| Remaining uncertainty | No inventory observations were provided. |

These are explanations of the **existing candidate group**, not a second approval object. The operator can inspect original passages, edit candidates, accept the whole dependency-complete group, defer or reject. Reuse prior confirmed decisions; do not request separate confirmation for every field. Relationship mappings inferred from a foreign key still require business evidence before becoming ownership or responsibility claims.

核对卡先说“这个决定会怎样改变结果”，技术字段放在可展开的详细编辑中。缺口只限制依赖它的部分；没有当前库存不妨碍交付“可借”的定义，也不能被解释成库存为零。

### Authorized host review and maintenance / 已授权的宿主核对与维护

When the operator has already authorized a specific review or correction, the host can use the same transaction guards without opening a server or reverse-engineering browser tokens:

```bash
python -X utf8 scripts/knowledge.py --project "./work/equipment" --revision PROJECT_REVISION --operation-id OPERATION_ID review --group GROUP_ID --action accept --reason "Operator reviewed the stated meaning and evidence"
python -X utf8 scripts/knowledge.py --project "./work/equipment" review --group GROUP_ID --action defer --reason "The operator needs the missing source before accepting"
python -X utf8 scripts/knowledge.py --project "./work/equipment" edit --file "./work/revised-asset.json"
```

`review` requires an explicit action and reason. `--assets` optionally supplies a JSON array of revised assets belonging to that group; unrelated IDs are rejected. `edit` saves a draft unless `--confirm` is explicitly supplied under operator authorization. Both reuse ordinary evidence, dependency, fingerprint, revision and receipt checks. These commands do not authorize the host to invent approval or pass an observation. Never automatically retry a rejected group as accepted.

已有操作者授权时，可直接用 `review` 记录明确的接纳、拒绝或暂缓理由；`--assets` 可提交本组内修订资产。`edit --file` 默认保存草稿，只有操作者明确授权确认时才加 `--confirm`。仍执行相同的依据、依赖、版本及回执检查，不需要反查浏览器实现。命令可用不等于获得批准，不可伪造通过记录。

For a host that explicitly needs HTTP, open the local workbench URL printed by `start.py`, read the same-origin page's `meta[name="session-token"]`, and send its value as `X-Workbench-Token` on API requests. A browser on that page can use `document.querySelector('meta[name="session-token"]').content`; the page's `Origin` must remain the same local origin. The token is server-session scoped; do not copy it into source materials, shared files or external requests. Prefer the CLI when no browser session is needed. / HTTP 集成须从已打开的同源本机页面读取会话 meta，使用 `X-Workbench-Token` 头，保持同源；令牌只用于当前服务会话，不写入材料或分享文件。无需浏览器时优先用 CLI。

## Interpret checks / 怎样读检查结果

Scenario checks use the same task-resolution reader as independent packages. Decisions are not answer scores:

| `decision` / `status` | Next step |
| --- | --- |
| `needs_selection` | Inspect candidate meanings and select intended stable IDs. Follow candidate pagination if relevant. |
| `no_match` | Refine names/aliases or inspect existing definitions; if meaning is genuinely missing, obtain evidence and propose it. No match does not prove the entire business concept is absent. |
| `needs_review` | Inspect the specific gaps, applicability or incomplete context page. A declared gap may remain even when structural `request_complete` is true. |
| `context_available` | Inspect selected definitions, scope, dependencies and evidence. The full natural-language question still has `resolution.question_coverage: "not_verified"`. |
| `requires_execution` | Semantic context is available but the requested calculation, query or action needs a suitable authorized runtime. No execution occurred. |

Always inspect `next_steps`, `gaps`, `source_warnings`, `capabilities`, package draft/completeness and `request_complete`. Without selected IDs, candidate pagination is at the top level. With selected IDs, context pagination is inside `context`; follow its offset until the needed context is complete. These checks establish the inspected scope, not business approval or production readiness.

## Deliver and reuse / 交付与持续修订

From **Deliver selected semantics / 交付所选语义**, use the existing publication screen to review scope and publish. Required dependencies are added by the shared package builder. A scenario check never publishes automatically. Question text and acceptance notes are not automatically included in a knowledge-only ZIP. Use **Create question handoff** to explicitly include the question, scope/date and acceptance expectations; private notes and observations stay local. The independent `task` reader retains the exact exported request; see [question delivery](question-delivery.md). Semantic restrictions belong in reviewed assets/required rules so they travel with the package, not only in a private note.

The recipient does not need the authoring project or a running workbench:

```bash
python -X utf8 scripts/semantic_read.py --package "./delivery/equipment.zip" resolve --question "How many items are available to borrow in Lab L?" --intent query
python -X utf8 scripts/semantic_read.py --package "./delivery/equipment.zip" resolve --question "How many items are available to borrow in Lab L?" --id demo.available --intent query
```

The first call discovers candidates; the second uses an explicitly selected root and includes dependencies, evidence and gaps. Replace example IDs with actual discovery results. Neither call calculates a current count. Full command and result details: [Agent reader](agent-reader.md).

When a consumer reports a wrong interpretation, compare the original question, snapshot, scope/date, selected IDs and evidence. Propose the smallest supported correction through normal review. Recheck affected questions and original counterexamples on the new revision before claiming improvement. Do not automatically change confirmed semantics, rewrite expected answers or mutate an already issued snapshot. Human usability gains require observation of users; fewer commands alone do not prove “zero threshold.”
