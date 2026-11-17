## Description:

Helps verify that AI agent skills maintain consistent behavioral invariants across repeated executions, including shifts based on execution count, environmental conditions, delayed activation triggers, performance drift, audit-log integrity, and risk tier.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud)

### License/Terms of Use:


## Use Case:

Developers, security reviewers, and agent operators use this skill to analyze repeated skill executions for invariant violations, resource or side-effect drift, execution-count sensitivity, and trigger-based activation patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Monitoring may require repeated analysis or execution of skills that have side effects.

Mitigation: Use controlled test inputs and isolated execution conditions for skills with side effects.

Risk: Audit logs and behavior observations can contain sensitive data if collected from real workloads.

Mitigation: Keep audit logs scoped to non-sensitive data where possible and avoid retaining secrets or private workload content.

Risk: Finite run counts and sampled monitoring may miss delayed or conditional activation patterns.

Mitigation: Scale monitoring depth to the skill's risk tier and increase sampling to full monitoring when drift is observed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andyxinweiminicloud/skills/behavioral-invariant-monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes invariant violation logs, resource trend analysis, side-effect consistency assessment, trigger-sensitivity findings, and a consistency verdict.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
