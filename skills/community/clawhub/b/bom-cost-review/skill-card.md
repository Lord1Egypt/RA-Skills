## Description:

Reviews BOMs for cost, sourcing risk, supply exposure, cost-down opportunities, and tariff/logistics sensitivity, producing a structured BOM review with rollups, cost drivers, risk flags, and action items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

External users, sourcing teams, product managers, and hardware engineers use this skill to review BOM cost against targets, identify major cost drivers, flag supply risks, and prioritize cost-down actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: BOMs can contain confidential product cost, supplier, forecast, lifecycle, and sourcing information.

Mitigation: Review and redact sensitive BOM and sourcing data before sharing it with an agent or downstream system.

Risk: Incomplete or stale BOM data can lead to incorrect cost rollups, MOQ assessments, lifecycle flags, or cost-down recommendations.

Mitigation: Label missing fields, reconcile rollup totals against line items, and verify lifecycle, sourcing, lead-time, and forecast inputs before acting on recommendations.

## Reference(s):

- [Bom Cost Review ClawHub Skill Page](https://clawhub.ai/mohitagw15856/skills/bom-cost-review)
- [Bom Cost Review Homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/bom-cost-review.html)

## Skill Output:

**Output Type(s):** [text, markdown, analysis, guidance]

**Output Format:** [Structured Markdown with summaries, tables, risk flags, data gaps, and action items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cost rollups, top cost drivers, risk registers, cost-down candidates, and tariff or logistics sensitivity notes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
