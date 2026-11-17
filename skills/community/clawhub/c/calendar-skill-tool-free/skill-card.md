## Description:

通过 porteden CLI 帮助代理管理 Google 与 Outlook 日历，支持查询日历和事件，以及创建、更新和删除事件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Personal users, developers, and workflow operators can use this skill to inspect calendars, search events, and prepare calendar create, update, or delete operations through porteden. Users should confirm any write action before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill description and triggers include security-scanning and compliance language that does not match the calendar-management behavior.

Mitigation: Use the skill only for calendar operations and do not rely on it for security scanning, compliance audits, vulnerability testing, or encryption controls.

Risk: Calendar data and credentials may interact with external providers through porteden, Google, or Outlook services.

Mitigation: Confirm account, profile, event target, and credential handling before use, and avoid exposing API keys or calendar content in shared logs.

Risk: Create, update, and delete operations can modify calendar state.

Mitigation: Require explicit confirmation before executing write operations and review generated commands before running them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/calendar-skill-tool-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and structured calendar-operation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include calendar IDs, event details, command output, and confirmation prompts for create, update, or delete actions.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
