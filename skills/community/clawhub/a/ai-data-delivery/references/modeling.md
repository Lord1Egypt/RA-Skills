# From structure to a useful semantic model / 从结构到可复用语义

Use this when the user wants business meaning, not just an editable schema. The host handles IDs, JSON and CLI calls. Keep one local model; no saved question, server or separate SQL model is required.

## Show the part being edited

In an interactive session show the first useful graph, then a small change when its business meaning changes. Reuse the temporary local editor for the same project. Append `&focus=ACTUAL_ID#graph` or `&domain=URL_ENCODED_DOMAIN#graph` to the startup URL containing `?lang=...`. If reusing an open tab, follow a change chip, or open the new focus URL. Only present a screenshot from the actual saved project; include the project revision. Do not send private schema or screenshots to an outside service. Headless users can stay on CLI.

For a new business, distinguish a thing (object), a verb between two things (relation), and a condition, responsibility or deadline (rule). Reuse physical datasets/columns as mappings; absent columns stay gaps. The editor supplies type-specific endpoints and source citations. Use the graph to show both a supported fact and a material gap before asking for more documents.

## Work from the current task

Import the schema with `--seed-draft` only into an empty model, then import the business notes. `state --summary` finds source, batch and asset IDs without returning full project history. Read full `state` or the relevant `task --batch ID` once when exact fields and source fragments are needed; save that JSON locally rather than repeatedly pasting it into conversation.

Before authoring, identify the smallest useful meaning: business object and identity, counting grain, value/unit, time, included/excluded states, relationships, and explicit unknowns. Separate records from real objects (a person can have several roles; a meter reading is not consumption). Preserve 0, false and null. Derive meaning from supplied policy and evidence; examples are not business rules.

For a metric, use the exact required keys `unit`, `grain`, `inclusions`, `exclusions`, `time_scope`, each describing its own meaning briefly. For example, a fictional monthly paid-order metric could have `inclusions: "paid orders"`, `exclusions: "cancelled orders"`, `time_scope: "paid_day in July 2025"`; actual values must come from the user's policy. Copying the whole policy into every key leaves the meaning unstructured. Put business relationships in `relation` assets with evidence and a meaningful predicate. A physical foreign key establishes a reference, not ownership or authority. Describe cardinality, aggregation order or temporal conditions when the supplied policy makes them relevant; otherwise record the gap.

**The root is what the recipient will read.** Its `refs` must include the definitions, fields, mappings, relations and rules actually needed for the task, including connection keys and fields on secondary tables. A field that appears only in SQL text or elsewhere in the full package is not a declared dependency. Reuse existing IDs; do not copy a physical field into a second source of truth.

Examples of dependency checks, not default policies:

- An account balance may require contract currency plus balance date/version/amount and their join keys; contract fields alone are insufficient.
- A metered quantity may require readings, multiplier and an explicit rollover rule; the meter object alone is insufficient.
- Independent payment and certificate totals may need separate aggregation before joining. Do not invent a direct row join to make a graph connected.

Use business names and source-supported aliases which a recipient is likely to use. Keep evidence quotations focused on the assertion and include scope/exception clauses that qualify it. The importer conservatively reviews a changed surrounding fragment even when the quoted sentence remains; never clear that review just because the old quote still appears.

## Make a coherent change once

One wide row may describe a vehicle, a person and an inspection event. Give them separate identities when the sources support that distinction. Review the role of every ambiguous key with the operator. For obligations, preserve the issuer, applicable subjects, dates, conditions and required evidence where stated. When associating a metric, record its grain and compare the join against a duplicate example, such as two work orders for one incident. Keep missing links in `properties.knowledge_gaps`. A measure can help find cases to inspect without proving an individual case was completed.

When the owner or a held-out test gives a metric grain independently, pass that wording as `edit --file ASSETS.json --expect-grain "one incident ID"`. The batch must contain exactly one metric and may contain supporting objects. A differing grain rejects the entire write. The comparison normalizes whitespace and case. If the two phrasings may be synonymous, reconcile their meaning before retrying. A matching label still needs the duplicate example to test the calculation.

The [asset contract](m1-m2-contract.md) defines the fields and evidence identities. Reuse the imported source's returned `source_id`, `revision`, `extraction_id`, `fragment_id` and exact `quote`; do not substitute a manual assertion for imported policy. Prepare a JSON **array of complete assets**, including any existing draft dependencies which are being reviewed. The array may refer to other assets in the same array. Changes are atomic: one invalid item leaves the graph unchanged.

```bash
python -X utf8 scripts/knowledge.py --project MODEL state --summary
python -X utf8 scripts/knowledge.py --project MODEL --revision READ_REVISION edit --file ASSETS.json
python -X utf8 scripts/knowledge.py --project MODEL inspect --id ROOT_ID
```

Replace READ_REVISION with the project revision returned when you read the model used to prepare that file. New identities alone need no revision. For existing assets, use the original read revision; after a conflict compare and merge the two versions before retrying. Do not simply fetch a new number.

An edit without `--confirm` saves drafts. After review, when the user or operator has already authorized confirmation of these supported definitions, use the same array with `--confirm`; do not ask again or leave supported dependencies draft merely because several assets are involved. Unknown business decisions remain draft or explicit `knowledge_gaps`. Permission to inspect data is not by itself permission to confirm business policy.

When a formal candidate decision is wanted, use existing `propose --batch ID --file GROUPS.json` and `review --group ID --action accept --reason TEXT` instead. Do not force both authoring paths on one task. An uncertain write is recovered with its operation receipt; do not replay a different payload under that operation ID.

`inspect` is read-only. It lists unconfirmed dependencies, existing omitted mappings/relations, omitted join keys, free-form SQL and newer source evidence. Add only relevant links to root `refs`, or explain why an advisory does not apply. It cannot discover every unstated business dependency or validate prose against a query. Cross-check the actual plan against the selected fields and sources yourself.

## Finish with one independently readable package

```bash
python -X utf8 scripts/knowledge.py --project MODEL export --id ROOT_ID --out NEW_PACKAGE.zip
python -X utf8 scripts/semantic_read.py --package NEW_PACKAGE.zip context --id ROOT_ID --detail full
python -X utf8 scripts/semantic_read.py --package NEW_PACKAGE.zip sources --id ROOT_ID
```

Use an existing output directory and a new file name. Export `--draft` only when the intended handoff is explicitly a draft. Read required context pages and the exact source evidence; compare the delivered IDs with the fields/relationships needed by the task. `complete` is structural coverage of declared dependencies, not business correctness. Missing rows or a production executor do not make a semantic handoff fail; report the separate execution requirement honestly.

Open `start.py --project MODEL` only if the user benefits from inspecting or editing the graph. Stop the temporary editor when finished. Do not add accounts, a service layer, mandatory checklists or a second model to accomplish this workflow.

中文提示：先围绕当前业务任务建最小语义；让主指标一次引用齐实际所需的字段、连接键、映射、关系和规则。用数组成组维护，复用已有确认授权；`inspect` 帮助发现遗漏，但不替人判断业务。导出后由独立读取进程核对来源与范围，用户只处理真正影响含义的决定。
