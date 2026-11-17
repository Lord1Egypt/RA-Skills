## Description:

Dingtalk CLI SKILL helps agents use the dws command-line tool to manage DingTalk AI tables, calendars, contacts, chat bots, todos, approvals, attendance, reports, DING messages, and workbench apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cizixiu](https://clawhub.ai/user/cizixiu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, operators, and developers use this skill to route DingTalk workplace requests to documented dws CLI commands and helper scripts. It supports common workflows such as querying schedules and attendance, managing todos and AI table records, sending chat or DING messages, reviewing reports, and recovering from CLI errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill combines broad DingTalk workplace data access with commands that can mutate records, messages, approvals, and membership.

Mitigation: Install only in organizations that trust the dws CLI publisher and grant the minimum DingTalk permissions needed for the intended workflows.

Risk: Mutable installer guidance or unverified binaries can expose users to supply-chain risk.

Mitigation: Prefer the pinned installer path in SKILL.md, verify the documented SHA-256 before use, and avoid running mutable main-branch installer commands directly.

Risk: Client secrets and DingTalk tokens can expose workplace data if mishandled.

Mitigation: Store DWS_CLIENT_ID, DWS_CLIENT_SECRET, DWS_CONFIG_DIR, and DWS_SERVERS_URL values in an approved secret manager or protected agent environment.

Risk: High-impact actions such as deletes, approvals, broadcasts, @all messages, attendance or contact lookups, report sends, and attachment uploads can affect other users or disclose sensitive data.

Mitigation: Require explicit human confirmation before these actions and review the target IDs, recipients, files, and message content before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cizixiu/skills/dingtalk-cli-skill)
- [dws CLI releases](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/releases/latest)
- [Global reference](references/global-reference.md)
- [Intent routing guide](references/intent-guide.md)
- [Field and high-risk operation rules](references/field-rules.md)
- [Error codes and agent behavior](references/error-codes.md)
- [Recovery guide](references/recovery-guide.md)
- [AI table commands](references/products/aitable.md)
- [Calendar commands](references/products/calendar.md)
- [Chat and bot commands](references/products/chat.md)
- [Contact commands](references/products/contact.md)
- [Todo commands](references/products/todo.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline dws shell commands, Python helper scripts, and JSON-oriented CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the dws binary and DingTalk credentials configured through DWS_CLIENT_ID, DWS_CLIENT_SECRET, DWS_CONFIG_DIR, and DWS_SERVERS_URL.]

## Skill Version(s):

1.0.13 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
