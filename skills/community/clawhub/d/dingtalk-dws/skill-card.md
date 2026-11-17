## Description:

Provides guidance, command routing, and helper scripts for agents to use the DingTalk dws CLI across AI tables, calendar, contacts, chat bots, todos, approvals, attendance, reports, DING messages, and workbench tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cizixiu](https://clawhub.ai/user/cizixiu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and business operations agents use this skill to inspect, create, update, and recover DingTalk workplace workflows through the dws CLI. It is intended for authenticated DingTalk environments where the agent has been granted the required app scopes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can act across sensitive DingTalk business data and communication workflows.

Mitigation: Install only after trusting the publisher and confirming the DingTalk app scopes granted to the CLI.

Risk: Client secrets, OAuth credentials, and webhook tokens may be exposed through prompts, logs, or shell history.

Mitigation: Keep secrets out of chat, command arguments, logs, and shared machines; use the configured environment variables only in controlled environments.

Risk: Commands can send messages, upload files, book rooms, approve or delete records, or trigger paid DING actions.

Mitigation: Require explicit user confirmation before message sends, approvals, deletes, paid DING calls, room bookings, and file uploads.

Risk: A mutable installer or unverified binary can change independently of this skill release.

Mitigation: Prefer the pinned dws archive and verify its SHA256 hash before use.

## Reference(s):

- [Dingtalk CLI SKILL on ClawHub](https://clawhub.ai/cizixiu/skills/dingtalk-dws)
- [dws CLI latest release](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/releases/latest)
- [Pinned dws Windows AMD64 archive](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/releases/download/v1.0.8/dws-windows-amd64.zip)
- [Global Reference](references/global-reference.md)
- [Intent Routing Guide](references/intent-guide.md)
- [Recovery Guide](references/recovery-guide.md)
- [Error Codes](references/error-codes.md)
- [Field Rules](references/field-rules.md)
- [AI Table Command Reference](references/products/aitable.md)
- [Calendar Command Reference](references/products/calendar.md)
- [Chat and Bot Command Reference](references/products/chat.md)
- [Todo Command Reference](references/products/todo.md)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline dws commands, JSON-oriented command outputs, and Python helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the dws binary and DingTalk credentials through DWS_CLIENT_ID, DWS_CLIENT_SECRET, DWS_CONFIG_DIR, and DWS_SERVERS_URL.]

## Skill Version(s):

1.0.12 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
