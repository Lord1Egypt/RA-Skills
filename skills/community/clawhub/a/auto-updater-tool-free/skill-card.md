## Description:

智能自动更新工具-免费版 guides agent-assisted version checks, differential updates, backups, rollbacks, update logs, and scheduled checks for personal project maintenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and individual maintainers use this skill to guide update workflows for personal projects and configuration files. It helps an agent check remote versions, apply differential updates, create backups, roll back changes, and report update history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to run commands, fetch remote content, and modify local files.

Mitigation: Use it only in a test or non-sensitive project and require explicit confirmation before update, sync, rollback, or callback actions.

Risk: Scheduled checks and callback scripts can create persistent or under-scoped command execution.

Mitigation: Do not enable cron jobs or callback scripts until the exact commands have been inspected and constrained to approved paths.

Risk: The advertised triggers are broader than update-specific workflows.

Mitigation: Invoke it only for explicit version-check, update, sync, backup, rollback, or update-history tasks.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that modify local files, fetch remote content, create backups, schedule checks, or run callback scripts; require confirmation before execution.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
