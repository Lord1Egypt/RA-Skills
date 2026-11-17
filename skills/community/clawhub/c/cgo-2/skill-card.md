## Description:

AI CGO helps agents diagnose growth bottlenecks, design AI-driven growth workflows, and optimize funnels using revenue, conversion, retention, and cost metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qomob](https://clawhub.ai/user/qomob)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, consultants, and growth teams use this skill to turn business context and growth challenges into metric-linked diagnoses, workflow designs, optimization plans, KPI systems, and experimentation loops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may retain growth context and update local learning or router files with user-derived business information.

Mitigation: Avoid sharing proprietary metrics or customer-specific strategy unless the runtime asks before saving and provides a chance to review, edit, or roll back saved entries.

Risk: The security verdict is suspicious because persistence behavior is not sufficiently contained or validated.

Mitigation: Review saved learning and routing changes before deployment, and keep sensitive business data out of persistent skill files unless approved.

## Reference(s):

- [Source repository (qomob/cgo)](https://github.com/qomob/cgo)
- [ClawHub skill page](https://clawhub.ai/qomob/skills/cgo-2)
- [AI CGO Capability Model](references/capability-model.md)
- [Harness Engineering Framework](references/harness-engineering.md)
- [AI CGO Growth Workflow Design](references/workflow-design.md)
- [AI CGO Knowledge Base](learnings/kb.md)
- [Router Signal Table](learnings/router-signals.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown with structured sections, tables, assumptions, KPI details, and execution metrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include business assumptions, growth benchmarks, workflow architecture, experiment plans, and session-level routing metrics.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
