## Description:

Cron System Manager guides agents in checking cron task status, updating task configuration, detecting duplicate responsibilities, and optimizing scheduled task assignments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianheihei002](https://clawhub.ai/user/tianheihei002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace operators use this skill to manage personal cron workflows, including status checks, task role separation, notification rules, retries, and incident cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs the agent to run checks on every message and make automatic workspace or task-configuration changes without clear user approval.

Mitigation: Install only in a controlled personal workspace, narrow activation to explicit cron-management requests, and require approval before file writes, task prompt changes, retries, timeout changes, notifications, or deletion of incident records.

## Reference(s):

- [Cron System Manager on ClawHub](https://clawhub.ai/tianheihei002/skills/cron-system-manager)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with task matrices, checklists, and inline path and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose workspace file edits, cron prompt changes, retries, timeout changes, notifications, and incident record cleanup.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
