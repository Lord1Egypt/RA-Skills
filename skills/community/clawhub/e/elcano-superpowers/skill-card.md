## Description:

Elcano Superpowers guides agents through a structured development workflow for larger code changes using brainstorming, planning, sub-agent execution, review, and shipping steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elcanoclaw](https://clawhub.ai/user/elcanoclaw)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to manage larger features, refactors, and multi-file changes with an approved design, small TDD-oriented tasks, sub-agent implementation, and final review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow includes deployment-affecting actions such as git push, PM2 restarts, and broad git checkout operations without a clear final approval gate.

Mitigation: Review the skill before installing in shared, staging, or production-connected repositories, and require explicit user approval before push, restart, or broad checkout actions.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown guidance with inline commands and task templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce plans, review checklists, implementation prompts, commit commands, and deployment-style steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
