## Description:

Creates software implementation plans, with optional file-based state for unresolved decisions and multi-phase recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iliaal](https://clawhub.ai/user/iliaal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to turn software requests into scoped, verifiable implementation plans and preserve decisions or recovery state when work spans phases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The partial security scan could not assess the underlying Python script and flagged a possible mismatch between evaluation or diagnostic commands and the planning purpose.

Mitigation: Review the reported commands and unresolved local path before running them, and confirm they fit the intended planning task.

## Reference(s):

- [Plan Format](artifact/references/plan-format.md)
- [Task Design](artifact/references/task-design.md)
- [ClawHub Skill Page](https://clawhub.ai/iliaal/skills/compound-eng-planning)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Files]

**Output Format:** [Markdown implementation plans and task lists, optionally saved as planning files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May scaffold .plan/task_plan.md for durable working state]

## Skill Version(s):

5.1.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
