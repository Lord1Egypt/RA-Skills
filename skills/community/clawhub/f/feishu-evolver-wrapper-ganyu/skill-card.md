## Description:

Feishu-integrated wrapper for the capability-evolver that manages the evolution loop lifecycle, sends Feishu card reports, and provides dashboard visualization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foras910521-lab](https://clawhub.ai/user/foras910521-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run and supervise a capability-evolver loop with Feishu reporting, dashboard output, lifecycle controls, and watchdog restart support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-running autonomous execution and watchdog restart behavior can persist beyond a single task.

Mitigation: Enable it only in an intended evolver workspace, review lifecycle and watchdog settings, and disable auto-restart paths when continuous operation is not required.

Risk: Git sync behavior can commit, pull, rebase, and push workspace state.

Mitigation: Use a repository with least-privilege credentials, review generated commits before publication, or disable Git sync in sensitive workspaces.

Risk: Feishu reporting and raw history export can send local logs or memory-derived content outside the workspace.

Mitigation: Configure Feishu targets deliberately, review report and export paths, and avoid running the skill in workspaces containing secrets or private memory.

Risk: Auto-heal and dependency installation behavior can modify sibling skills or install packages.

Mitigation: Review auto-heal settings and dependency installation paths before use, and restrict filesystem permissions when evaluating the skill.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, Feishu card payloads, shell commands, and local JSON/log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run long-lived lifecycle processes and write workspace logs, reports, PID files, and Feishu document or message updates.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
