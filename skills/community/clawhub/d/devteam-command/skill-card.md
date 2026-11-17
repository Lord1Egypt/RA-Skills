## Description:

Runs a full Dev Team pipeline from planning to release for coding tasks, producing plans, code, tests, fixes, and release notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunlearndev](https://clawhub.ai/user/sunlearndev)

### License/Terms of Use:


## Use Case:

Developers use this skill to coordinate a multi-agent coding workflow for scoped repository tasks, from planning and implementation through testing and release notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger a broad, long-running multi-agent coding workflow that may modify repository code.

Mitigation: Use it only for clearly scoped repository tasks, avoid concurrent runs, and review all code changes before accepting them.

Risk: Advertised fixer and documentation outputs may not be produced reliably.

Mitigation: Confirm generated PLAN.md, TASKS.md, BUGS.md, RELEASE.md, and any fixes exist and match the task before relying on completion status.

## Reference(s):

- [DevTeam Command on ClawHub](https://clawhub.ai/sunlearndev/skills/devteam-command)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files and code changes with command and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May spawn long-running subagents and should be used only for clearly scoped repository tasks.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
