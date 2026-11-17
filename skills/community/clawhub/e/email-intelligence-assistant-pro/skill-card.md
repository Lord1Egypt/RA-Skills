## Description:

Connects to IMAP mailboxes to classify emails by urgency, suggest multilingual replies, and push real-time summaries to Feishu chats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffersplind92](https://clawhub.ai/user/jeffersplind92)

### License/Terms of Use:

MIT-0

## Use Case:

Customer service teams and operators use this skill to monitor IMAP mailboxes, triage incoming messages by urgency, draft reply suggestions, and receive Feishu alerts or daily digests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive mailbox content and can share summaries or generated replies with configured AI and Feishu services.

Mitigation: Review and approve the data flows before connecting a real mailbox; avoid regulated or sensitive inboxes unless the organization has approved the AI and Feishu processors.

Risk: Mailbox credentials, AI API keys, Feishu webhook URLs, and Feishu app tokens are required for normal operation.

Mitigation: Use only app-specific mailbox passwords and scoped service credentials, store configuration outside public repositories, and rotate credentials if exposed.

Risk: The security guidance says not to rely on --dry-run to prevent pushes, and the artifact's main script still processes emails through the normal push path.

Mitigation: Disable Feishu push configuration during testing and verify behavior in an isolated mailbox before enabling scheduled runs.

Risk: The artifact includes unrelated token-validation behavior and external endpoint use.

Mitigation: Review the token verification path and allowed outbound endpoints before installation, especially before creating cron jobs or other recurring execution.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/jeffersplind92/skills/email-intelligence-assistant-pro)
- [Publisher profile](https://clawhub.ai/user/jeffersplind92)
- [YK-Global paid plans](https://yk-global.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and YAML configuration examples; runtime scripts can emit terminal text or JSON email summaries and Feishu card messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes mailbox content, uses configured AI API credentials, and can send email summaries or generated reply suggestions to Feishu when enabled.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
