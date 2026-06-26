---
name: bp-monthly-report-skill
description: Use when drafting a monthly BP report from a fixed template, BP period and node identifiers, and real BP or progress-report evidence. This skill enforces a staged workflow: normalize the template, map BP anchors, collect evidence, build fine-grained cards, then draft the report in a fixed section order instead of generating the whole report in one pass.
---

# BP Monthly Report Skill

Use this skill when the user wants a monthly report draft that must match a fixed structure and be grounded in real BP data, node progress, and business updates.

## Capability Summary

This skill can directly handle these tasks:

- identify the target BP node from a node name, `groupId`, or BP组织节点ID
- fetch the node's BP goals, key results, measure standards, and linked reports
- generate lightweight evidence manifests and direct report references
- generate staged artifacts, fine-grained KR/action cards, and a monthly or quarterly report draft
- roll a later month forward from the previous month's baseline
- use the bundled default month template and bundled fill-in specification when the environment has standardized on them

It is not only a writing guide. It is a BP-fetching and report-drafting workflow.

## First-Turn Behavior

On the first reply, state the skill's capability plainly and ask only for the minimum missing inputs.

Preferred opening pattern:

```text
我可以直接按 BP 系统取数并生成这份月报。
最少只需要这 3 个信息：
1. BP周期或 `periodId`
2. 节点名称、`groupId` 或 BP组织节点ID
3. 月报月份

如果模板和填报规范已经固定，我会直接按既定模板执行，不再重复询问。
如果你要，我先从节点解析和 BP 取数开始。
```

Do not describe the skill as if it were only a manual or passive guideline.
Do not ask for `月报模板` or `进展数据` again if the workflow is already designed to fetch evidence from the BP system itself.
Ask about template or spec only if:

- the user explicitly says a different template must be used
- the template is genuinely unknown for the current environment
- the report structure cannot be inferred from prior context

## Goal

Produce a controllable `v1.0` monthly report draft that:

- matches the target template structure exactly
- uses the user's fill-in convention and wording constraints
- is backed by traceable BP and progress evidence
- surfaces concrete work progress for each major item, not only evidence existence
- is generated section by section, not in one pass
- evaluates progress primarily through `关键成果 + 衡量标准`, not through `关键举措` volume
- exposes how many original work reports were adopted for the draft so source coverage can be judged quickly
- uses `汇报日期` as the only default month-attribution rule for monthly evidence selection

## What to read

1. Read the target month report template.
2. Read the user's fill-in specification or a completed sample based on that template.
3. Read only the BP and progress materials needed for the current node and person.
4. If the data layout is unclear, read [references/source-schema.md](references/source-schema.md).
5. For the staged workflow, read [references/workflow.md](references/workflow.md).
6. For section order and section writing rules, read [references/section-order.md](references/section-order.md).
7. If the user supplied a filled sample or fill-in convention, read [references/fill-patterns.md](references/fill-patterns.md).
8. When BP system fetching is involved, read [references/bp-system.md](references/bp-system.md).
9. When status judgment is required, read [references/traffic-lights.md](references/traffic-lights.md).
10. When producing deliverables, read [references/artifact-layout.md](references/artifact-layout.md).
11. When writing a later month or quarter, read [references/rolling-baseline.md](references/rolling-baseline.md).
12. When a Chinese business-facing explanation is needed, read [references/business-description.zh-CN.md](references/business-description.zh-CN.md).
13. When a Chinese design or architecture explanation is needed, read [references/design-solution.zh-CN.md](references/design-solution.zh-CN.md).

If the user does not provide another template package and the current environment uses the standard monthly pack, use these bundled defaults first:

- [assets/P001-T001-MONTH-TPL-01_月报模板_v1.md](assets/P001-T001-MONTH-TPL-01_月报模板_v1.md)
- [assets/人力资源中心_月报填写规范_组织示例_v1.md](assets/人力资源中心_月报填写规范_组织示例_v1.md)

## Non-negotiable rules

- Do not draft the full report in a single generation pass.
- Do not write section 1 before sections 2-8 are materially stable.
- Keep the final chapter order and heading structure identical to the target template.
- Every conclusion must be attributable to a BP anchor, a progress update, or an explicit user input.
- When evidence is missing, mark the field as missing and ask for补充 only if the gap blocks a reliable draft.
- Prefer deterministic intermediate artifacts over free-form reasoning.
- Ask for and confirm the `BP周期` and the `目标节点` before fetching BP data. If the user already provides `periodId` together with `groupId` or a BP组织节点ID, use them directly and skip redundant lookup.
- Treat `目标` as the desired end state, `关键成果` as the evaluation basis, and `关键举措` as supporting actions.
- Always fetch `关键举措` metadata together with goals and key results.
- In chapter 2, the traffic-light judgment target is each `关键成果`. Do not judge only at the goal heading level. If one subsection contains multiple key results, render separate result blocks and judge each one independently.
- In chapter 4, the traffic-light judgment target is each `关键举措`. Do not judge only at the chapter summary level. Each action block must carry its own `🟢 / 🟡 / 🔴 / ⚫` judgment.
- In report writing, prioritize evidence linked to goals and key results. Use action reports as secondary support for evaluation, but treat them as a major evidence pool for concrete progress extraction.
- When evaluating related reports, prioritize reports written by the current node's responsible owners or assignees. Reports written by others are only auxiliary evidence unless the user explicitly says otherwise.
- Every major BP item must carry a traffic-light icon judgment: `🟢 / 🟡 / 🔴 / ⚫`.
- Treat the traffic light as the single deviation signal. Do not add a second independent `偏离判断` color field.
- If no valid progress report or no credible evidence can support progress judgment for the current month, default to `⚫` rather than `🟡` or `🔴`.
- AI may judge an item as `⚫`, but AI must not decide the black-light subtype on its own.
- After a `⚫` judgment, the report must explicitly tell the user that black-light subtype requires manual review, and ask the user to choose one of: `未开展/未执行`, `已开展但未关联`, or `体外开展但体系内无留痕`.
- If the user confirms `未开展/未执行`, the report must explicitly ask and record what will be done in the next month / next cycle.
- If the user confirms `已开展但未关联`, the report must explicitly require BP re-association of the existing work report/material and keep that item as a reminder until the next cycle confirms completion.
- If the user confirms `体外开展但体系内无留痕`, the report must explicitly require补充留痕 and improvement of the working method so the same level can be judged in future cycles.
- Every traffic-light judgment in the final report must be followed by an explicit `判断理由`.
- In user-facing report markdown, render the whole traffic-light review block in a color that matches the judgment itself: `🟢` uses green text, `🟡` uses yellow text, `🔴` uses red text, and `⚫` uses black or deep gray text.
- Every traffic-light judgment in the final report must also include a short human-review block asking whether the user agrees with the judgment.
- The human-review block must support: `同意 / 不同意`.
- If the reviewer disagrees, the block must ask for a reason category and free-text reason.
- Reason categories should at least support: `BP不清晰` / `举证材料不足` / `AI判断错误` / `其他`.
- If the judgment is `🟡` or `🔴` or `⚫`, the final report must require a corrective-action block: `整改方案` / `承诺完成时间` / `下周期具体举措`.
- Every adopted evidence item in the final report must point to the original BP report itself, preferably via `[标题](reportId=<id>&linkType=report)`. Do not dump full report bodies into local JSON files unless the user explicitly asks for archival snapshots.
- Until upstream APIs expose stable attachment metadata and `reportId`, treat attachment reading and direct online links as pending integrations instead of fabricating local substitutes.
- For each major report item, extract concrete progress lines from the source report: what was completed, what moved forward, what decision was made, what remains blocked, and what happens next.
- When raw report payloads expose attachment metadata or attachment links, record that metadata together with the evidence entry and read the attachments before drafting if they materially affect progress judgment.
- Do not reduce a chapter to “there is evidence”. Convert evidence into explicit progress statements.
- Section 1 must state how many original work reports were adopted for this draft. Prefer a compact breakdown such as total adopted reports, owner-authored primary reports, other manual reports, and AI reports if any were used.

## Required inputs

At minimum, gather:

- reporting month
- BP period or `periodId`
- reporting node or node identifier such as `groupId`, `node_id`, or an unambiguous node name

Default minimum call contract:

- `period_id` or `bp_period`
- `groupId` or `node_id` or `node_name`
- `report_month`

Ask for template path, spec path, or extra progress materials only when they are actually missing for the current environment.

Optional but useful:

- person name, role, department, if the template metadata or node resolution needs it
- employeeId, if the node is a personal BP node and is easier to resolve this way
- explicit BP IDs for the node
- management summary or leader concerns for the month
- optional wording preferences for rendering traffic-light explanations

Usually do not require these optional fields before starting BP fetch and evidence collection.

## Working sequence

Follow this sequence without collapsing steps:

1. Confirm the BP period and target node.
2. Normalize the template and extract the exact heading tree.
3. Resolve the node inside BP and build a BP anchor map.
4. Collect month-specific evidence and map each fact to a BP anchor.
   - Prefer using `scripts/collect_bp_month_evidence.py` instead of ad hoc query code.
5. Build section cards before writing any chapter prose.
   - Prefer using `scripts/dump_bp_anchor_map.py` to stabilize the BP skeleton.
6. Materialize dual-report artifacts.
   - Prefer using `scripts/build_dual_report_artifacts.py` to create `04_cards / 05_ai_baseline_report / 05_review_queue / 07_user_review_report`.
7. Draft sections in this order: `2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 1`.
8. Run a consistency pass to check wording, metrics, status, and cross-section alignment.

## Expected intermediate artifacts

Create these artifacts in memory or as working notes:

- `intake_summary`
- `template_outline`
- `bp_anchor_map`
- `evidence_ledger`
- `04_cards`
  - `kr_cards`
  - `action_cards`
- `05_review_queue`
- `05_ai_baseline_report`
- `07_user_review_report`
- `source_inventory_summary`

Use the field definitions from [references/source-schema.md](references/source-schema.md).

Persist the run artifacts using the layout from [references/artifact-layout.md](references/artifact-layout.md).

## Output standard

The final output should include:

- a short note on what sources were used
- the monthly report draft with the exact template structure
- a short gap list for fields that still need manual补数 or确认

Do not add extra chapters unless the user explicitly asks for them.
