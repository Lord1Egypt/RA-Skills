## Description:

AI coding disciplines that maintain an evolving record of prior mistakes to reduce repeated coding errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[9438190](https://clawhub.ai/user/9438190)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to enforce disciplined coding workflows, maintain project logs, test boundary cases, and record repeated error patterns as future safeguards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives itself broad automatic control over coding workflow and future rule changes.

Mitigation: Review before installing and require human review for self-updates, generated logs, and workflow changes before accepting them.

Risk: The skill includes unsafe file mutation and deletion instructions, including a rule to delete project_data.db during testing.

Mitigation: Remove the deletion rule or make it explicitly opt-in before using the skill in repositories where project_data.db may contain valuable data.

Risk: The skill can create project files and log task details as part of its required workflow.

Mitigation: Use only in repositories where persistent workflow logs are acceptable and review logged content for sensitive information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/9438190/skills/coding-disciplines)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline commands and workflow checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to create project files, update logs, synchronize plan state, run validation commands, and record new workflow rules.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
