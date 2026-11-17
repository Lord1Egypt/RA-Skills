## Description:

Routes Feishu task requests so an agent can create and update tasks, execute polled or recurring tasks, register the Feishu task agent, and refresh a daily.json profile from daily notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckyterry](https://clawhub.ai/user/luckyterry)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operators use this skill to turn action items, deliverables, follow-ups, task breakdowns, and recurring requests into Feishu tasks. It also supports Feishu task-agent registration and daily.json profile refreshes from the latest daily report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent task automation can create or update Feishu tasks and run recurring workflows without enough visible user control.

Mitigation: Use only where Feishu task automation is intended, and require explicit permission declarations plus separate confirmation for each persistent change.

Risk: AGENTS.md routing changes can steer future agent behavior beyond the immediate request.

Mitigation: Review proposed AGENTS.md changes before installation and provide a clear rollback path for removing the routing rule.

Risk: Scheduler metadata can make recurring behavior hard to audit if it is hidden from users.

Mitigation: Expose cron job names, schedules, messages, and uninstall or rollback instructions to operators before enabling scheduled workflows.

## Reference(s):

- [Feishu Task Agent](SKILL.md)
- [Feishu Task Orchestration Workflow](workflows/auto-task.md)
- [Polled Task Execution Workflow](workflows/polled-task-execution.md)
- [Feishu Task Agent Registration Workflow](workflows/reg.md)
- [Agent Profile and daily.json Workflow](workflows/agent-profile.md)
- [Feishu Auto Task Decision Rules](references/task-decision-rules.md)
- [Creator / Members Output Contract](references/task-output-contract.md)
- [daily.json Data Structure](references/profile-data-shape.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON payloads, and Feishu task updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update Feishu tasks, comments, attachments, cron jobs, AGENTS.md routing text, and daily.json profile data when the required tools are available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
