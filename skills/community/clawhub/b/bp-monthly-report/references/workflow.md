# Workflow

This workflow is designed to make the monthly report controllable and reproducible.

## Stage 0: Intake

Collect the minimum inputs:

- reporting month
- BP period
- node identity

Default minimum intake should be treated as:

- reporting month
- BP period
- node identity

`node identity` can be any of:

- node name
- `groupId`
- BP组织节点ID

Only ask for these additional items when they are truly unknown in the current environment:

- template file
- fill-in specification or completed sample
- BP source
- progress or business report source

## Intake response rule

The first user-facing response in this workflow should:

- say clearly that the skill can fetch BP and linked reports by itself
- ask only for the minimum missing inputs
- avoid restating the whole workflow before any work starts

Bad example:

- “这个技能需要几个关键信息，我先梳理一下……”
- “这个技能是一套操作指南……”

Preferred example:

- “我可以直接按 BP 系统取数并生成月报。先给我 `BP周期 + 节点 + 月报月份`，我先开始取数和建骨架。”

Output:

- `intake_summary`

## Stage 1: Template normalization

Extract:

- chapter titles
- subsection titles
- repeated field labels
- any mandatory phrasing patterns

Also record which sections are summary sections and which are evidence-driven sections.

Output:

- `template_outline`

## Stage 2: BP anchor mapping

For the current node, map:

- periodId
- groupId
- personal BP ID
- organization BP IDs
- target statement
- target metrics
- milestone or deadline
- key-result measure standards
- goal owners
- key-result owners
- action assignees
- action ids and action names

For chapter 2, the mapping must preserve the relationship:

- section heading -> goal
- goal -> one or more key results
- key result -> measure standard -> linked evidence

Do not collapse multiple key results into a single section-level light by default.

This step should be driven by the BP system's real object model:

- goal = target state
- key result = achievement evidence
- measure standard = evaluation basis
- action = supporting path

This produces the stable skeleton of the report.

Output:

- `bp_anchor_map`
- `bp_anchor_map` must preserve key-result-level judgment units for chapter 2

## Stage 3: Evidence collection

Pull only month-relevant evidence from BP updates, progress reports, meeting notes, or operating data.

When using BP system data, prioritize:

1. goal and key result detail
2. key result `measureStandard`
3. reports linked to goals and key results
4. action detail and reports linked to actions
5. action detail as support only for evaluation, but as a major evidence pool for concrete progress extraction

Each evidence entry should answer:

- what happened
- when it happened
- which BP it supports
- whether it is attached to a goal, key result, or action
- whether it is a result, action, deviation, risk, or next-step signal
- whether the fact is quantified
- who wrote the source report
- whether the author is the current owner or assignee
- what concrete progress was achieved
- what remains in progress
- what problems or blockers were exposed
- what attachments were available and whether they were read

Output:

- `evidence_ledger`
- `source_inventory_summary`

## Stage 4: Card assembly

Before drafting prose, build structured cards.

There should be two card layers:

- `04_cards`: AI structure cards
- `05_review_queue`: user review cards for `🟡 / 🔴 / ⚫`

Each structure card should contain:

- target heading
- source BP anchors
- evidence lines
- concrete progress points
- measure-standard based judgment
- owner-authored evidence priority
- adopted report count and source-coverage note
- traffic light
- missing fields
- suggested wording constraints

This is the main control point. If the cards are weak, the draft will drift.

Output:

- `04_cards`
- `05_review_queue`

## Stage 5: Fixed-order drafting

Write chapters in dependency order:

1. section 2: BP承接与对齐
2. section 3: 核心结果与经营表现
3. section 4: 关键举措推进情况
4. section 5: 问题、偏差与原因分析
5. section 6: 风险预警与资源需求
6. section 7: 下月重点安排
7. section 8: 需决策/需协同事项
8. section 1: 汇报综述

Reason:

- section 2 is built on goals and key results
- section 3 judges achievement against result standards
- section 4 is intentionally action-secondary
- sections 5-6 extract negative signals from that spine
- sections 7-8 depend on gaps, risks, and pending work
- section 1 is an executive summary and should be written last
- section 1 should explicitly state how many original work reports were adopted, because this is the user's quick coverage check

Output:

- `05_ai_baseline_report.md`

## Stage 6: Cross-check

Check:

- every summary statement appears in the evidence ledger
- the reported adopted-work-report count matches the adopted source inventory
- the reported raw-hit count matches the pre-collapse evidence scan
- every claimed progress point can be traced to an original BP report link or, if `reportId` is unavailable, to the adopted report title plus task and author metadata
- every traffic-light judgment is explainable from evidence
- every traffic-light judgment in the final report is followed by a visible status-colored `判断理由`
- every traffic-light judgment in the final report is followed by a human-review block
- every `🟡 / 🔴 / ⚫` judgment in the final report is followed by `整改方案` / `承诺完成时间` / `下周期具体举措`
- every `🟡 / 🔴 / ⚫` judgment also has a dedicated review card in `05_review_queue`
- the user may edit any part of the review report, but `🟡 / 🔴 / ⚫` blocks must not remain unexplained in the user review version
- every section 4 key action item carries its own traffic-light judgment; do not leave section 4 as a light-free narrative list
- every `⚫` judgment explicitly records a black-light subtype: `未开展/未执行` / `已开展但未关联` / `体外开展但体系内无留痕`
- every `⚫ 已开展但未关联` item is kept as a carry-forward reminder until the next cycle confirms BP association is completed
- every `⚫ 体外开展但体系内无留痕` item states what record-keeping change is required so future cycles can judge the same layer
- next month priorities align with unresolved items and milestones
- issue and risk sections do not contradict the overall judgment
- headings and order exactly match the template
- all required template chapters are present, especially sections 7 and 8 before section 1 is finalized
- conclusions do not over-rely on reports written by non-owners
- every adopted source link points to the original BP report when `reportId` is available; do not require local JSON snapshots
- attachment usage is explicit: read, unavailable from API, or not needed
- mass-distributed notices are not counted as separate adopted evidence entries just because the receivers differ

Output:

- `review_notes`
- `07_user_review_report.md`

## When to stop and ask

Ask the user only if one of these blocks the draft:

- the target template is ambiguous
- BP anchors for the node cannot be identified
- the month-specific evidence is too thin to support even section 2
- the reporting period is unclear
