## Description:

Comind guides agents through CoMind task execution, Markdown synchronization, conversation collaboration, status reporting, scheduling, and progress-check workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dqalex](https://clawhub.ai/user/dqalex)

### License/Terms of Use:


## Use Case:

Developers and AI operators use this skill to connect an agent to a trusted CoMind workspace, manage assigned tasks and deliveries, synchronize Markdown records, respond to chat and schedule contexts, and report status through CoMind workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad always-on authority to use CoMind API tokens and modify shared CoMind records.

Mitigation: Install only for a trusted CoMind workspace, use a narrowly scoped and revocable token, and require confirmation before write operations or credential-management actions.

Risk: Heartbeat and Markdown synchronization can publish workspace Markdown content into CoMind records.

Mitigation: Disable or review heartbeat document sync unless every Markdown file in scope is safe to publish.

Risk: A misconfigured CoMind endpoint could send the agent's token or actions to an untrusted service.

Mitigation: Set COMIND_BASE_URL only to a trusted HTTPS or loopback endpoint.

Risk: Remote execution instructions and token or member-management actions are admin-sensitive.

Mitigation: Review these instructions before execution and require explicit approval before credential or member-management operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dqalex/skills/comind)
- [CoMind homepage](https://github.com/comind)
- [Project chat context template](references/chat-project.md)
- [Schedule chat context template](references/chat-schedule.md)
- [Task chat context template](references/chat-task.md)
- [Document delivery template](references/deliveries.md)
- [Task list document template](references/doc-template-task-list.md)
- [Heartbeat progress-check template](references/heartbeat-check-progress.md)
- [Heartbeat daily-report template](references/heartbeat-daily-report.md)
- [Heartbeat status-sync template](references/heartbeat-sync-to-comind.md)
- [Schedule management template](references/schedules.md)
- [System information template](references/system-info.md)
- [Task board template](references/task-board.md)
- [Task push template](references/task-push.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON action examples, shell command examples, and Markdown templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires COMIND_BASE_URL and COMIND_API_TOKEN for CoMind API-backed workflows.]

## Skill Version(s):

2.3.4 (source: server release metadata; artifact frontmatter reports comind_version 2.2.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
