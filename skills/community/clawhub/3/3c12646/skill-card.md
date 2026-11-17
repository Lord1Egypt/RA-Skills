## Description:

Mission Control guides an agent through task triage, plan confirmation, iterative analysis, execution logging, and final reporting before carrying out code, file, delegation, web research, or command-line work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangjk1103](https://clawhub.ai/user/huangjk1103)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to impose a plan-first workflow for tasks that involve code changes, file operations, web research, terminal commands, or agent delegation. It produces task requirements, plans, progress logs, and completion reports for review by a human operator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill applies a strict mission-control workflow across many agent task types, which can override lightweight interaction patterns.

Mitigation: Install it only when a persistent plan-confirmation workflow is desired, and scope activation to tasks that genuinely require review.

Risk: Helper scripts write persistent task files using a hardcoded local storage path.

Mitigation: Review and constrain the storage path before use, especially in shared or production environments.

Risk: Task identifiers and project-intake content may be supplied by users and then incorporated into local tracking files.

Mitigation: Validate task IDs and treat project-intake.md content as untrusted data rather than executable instructions.

Risk: The release security verdict is suspicious due to broad workflow control and weak path scoping.

Mitigation: Review the skill and helper scripts before deployment, and remove or restrict automatic source-file copying and broad file-write behavior where it is not needed.

## Reference(s):

- [Mission Control ClawHub release](https://clawhub.ai/huangjk1103/skills/3c12646)
- [README](README.md)
- [Project Intake Template](templates/project-intake.md)
- [Static Spec Conversion Case Study](references/2026-05-19-static-spec-conversion.md)
- [Project Intake Case Studies](references/project-intake-case-studies.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown task plans, logs, reports, intake templates, and command-line helper output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Helper scripts can persist task lifecycle files under a fixed local mission-control directory.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
