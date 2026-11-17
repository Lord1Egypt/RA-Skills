## Description:

DingTalk Todo CLI helps agents manage DingTalk todos and task workflows with the authenticated dws CLI, including task creation, tracking, DING notifications, calendar follow-ups, and AI Sheet updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lm203688](https://clawhub.ai/user/lm203688)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, operators, and developers use this skill to create, assign, track, and escalate DingTalk tasks through repeatable CLI workflows. It is suited for standups, task delegation, overdue follow-up, sprint planning, and meeting action-item capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate through an authenticated DingTalk CLI account with broad access to tasks, contacts, sheets, calendars, bots, drive, approvals, and raw API calls.

Mitigation: Use a least-privileged DingTalk account, verify authentication status before workflows, and pin and verify the dws CLI version before use.

Risk: Raw dws API calls could access endpoints beyond the wrapped task-management commands.

Mitigation: Require explicit user approval for each raw API endpoint and method before execution.

Risk: DING escalation can notify managers, directors, HR, groups, or external platforms and may conflict with the skill's own confirmation rule.

Mitigation: Require confirmation before manager, director, HR, group, or external-platform DINGs, and apply the skill's rate limit and working-hours rules.

## Reference(s):

- [DingTalk Todo CLI on ClawHub](https://clawhub.ai/lm203688/skills/dingtalk-todo-cli)
- [lm203688 publisher profile](https://clawhub.ai/user/lm203688)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require the authenticated dws CLI and user approval for sensitive actions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
