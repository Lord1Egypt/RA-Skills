## Description:

自动生成每日邮件摘要，支持主流邮箱，快速了解重要邮件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

个人用户、独立开发者和企业团队 use this skill to access supported mailbox services through an agent/browser workflow and produce a daily digest with unread counts, sender and subject summaries, screenshots, and suggested follow-up actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent and browser automation environment to access email accounts, which can expose private mailbox content.

Mitigation: Use only accounts you are comfortable exposing to the agent environment and review the generated digest before sharing or storing it.

Risk: Password-entry command examples can expose credentials in command history, logs, or prompts.

Mitigation: Prefer an already logged-in browser session and do not type real passwords into command examples or agent prompts.

Risk: Generated screenshots may contain private email content.

Mitigation: Delete, encrypt, or otherwise protect generated screenshots and summary files after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/email-digest-tool-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Files]

**Output Format:** [Markdown and text reports with optional shell commands, JSON snippets, and screenshot files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local mailbox screenshots and summary files that can contain private email content.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
