## Description:

DingTalk CLI Auto helps agents automate DingTalk messaging, calendar, todo, contact, and robot webhook workflows through the DingTalk Workspace CLI and Node.js scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to operate DingTalk business workflows, including sending messages, creating meetings, managing todos, querying contacts, and posting robot notifications. It is intended for organizations that have configured a DingTalk internal app with appropriate permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance uses remote shell-piped installer commands that can execute unverified code.

Mitigation: Install only from pinned, verifiable DingTalk Workspace CLI releases or vetted package channels before using the skill.

Risk: Runtime command execution can expose users to unsafe local command execution when arguments are handled through a shell command string.

Mitigation: Use only trusted inputs until the command wrapper is changed to argument arrays without a shell.

Risk: DingTalk AppKey/AppSecret, OAuth state, robot webhooks, contact data, calendars, and todos are sensitive business access.

Mitigation: Use least-privilege DingTalk apps, keep secrets out of logs and prompts, and avoid production credentials until the security guidance is addressed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/onlyloveher/skills/dingtalk-cli-auto)
- [DingTalk Workspace CLI](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli)
- [DingTalk Open Platform](https://open.dingtalk.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require Node.js 18 or later, the dws CLI, DingTalk app credentials, and scoped DingTalk permissions.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
