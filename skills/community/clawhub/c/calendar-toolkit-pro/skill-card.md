## Description:

日历管理工具包专业版 helps agents manage enterprise calendar workflows, including multi-tenant calendars, resource booking, conflict checks, scheduling optimization, batch actions, and structured results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, enterprise teams, and automation users use this skill to let an agent create, query, export, analyze, and optimize calendar events, meetings, reminders, shared resources, and team schedules. It is intended for assisted calendar operations that still allow human review for consequential scheduling decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad command and file authority and includes examples for inspecting configuration variables.

Mitigation: Install with disabled or tightly scoped exec access, avoid exposing secrets, and require explicit approval before any local command or file operation.

Risk: Automated scheduling, exports, webhooks, and bulk operations could change or disclose calendar data at scale.

Mitigation: Use limited calendar and API credentials, restrict webhook destinations, test bulk actions on a small scope first, and require per-action confirmation for real calendars.

Risk: The security verdict is suspicious because user-control boundaries are not tightly defined.

Mitigation: Review the skill before deployment, document allowed actions, and monitor generated execution logs and audit records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/calendar-toolkit-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with JSON, text, bash, and Python examples; runtime responses are described as structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include execution status, result data, metadata, logs, and error fields.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
