## Description:

AI Chief Growth Officer routes growth diagnosis, opportunity exploration, workflow design, and optimization requests into structured AI growth plans focused on revenue, conversion, retention, and cost reduction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qomob](https://clawhub.ai/user/qomob)

### License/Terms of Use:

MIT-0

## Use Case:

Growth teams, founders, and business operators use this skill to diagnose growth bottlenecks, design AI-assisted growth workflows, audit funnels or systems, and produce metric-linked execution plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may share sensitive business metrics, customer details, strategy, or financial data during growth planning.

Mitigation: Share only the business data needed for the task and avoid storing confidential customer data, company-specific strategy, or raw financial details unless retention is intentional.

Risk: The skill can propose updates to knowledge-base or router-signal files as part of its learning workflow.

Mitigation: Confirm any proposed writes to kb.md or router-signals.md and review them for incorrect assumptions or weakened routing and safety behavior before applying.

Risk: Growth plans can become misleading when CAC, LTV, budget, PMF status, or funnel metrics are missing and the skill falls back to assumptions.

Mitigation: Provide real unit economics and business context where possible, and review all stated assumptions before acting on recommendations.

## Reference(s):

- [AI Chief Growth Officer Skill Page](https://clawhub.ai/qomob/skills/ai-cgo)
- [AI CGO Capability Model](references/capability-model.md)
- [Harness Engineering Framework](references/harness-engineering.md)
- [AI CGO Growth Workflow Design](references/workflow-design.md)
- [AI CGO Knowledge Base](learnings/kb.md)
- [Router Signal Table](learnings/router-signals.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Structured Markdown with growth diagnosis, workflow design, audit plans, KPI tables, execution metrics, and trace summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose knowledge-base or router-signal updates for user confirmation; uses session context for mode usage, assumptions, past outputs, and satisfaction signals.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
