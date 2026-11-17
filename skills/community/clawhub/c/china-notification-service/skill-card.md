## Description:

Implement multi-channel notification services for Chinese applications using WeChat Template Messages, WeChat Subscription Messages, SMS through Alibaba Cloud and Tencent Cloud, DingTalk Bot, Feishu Bot, and Email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lm203688](https://clawhub.ai/user/lm203688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to design multi-channel notification workflows for China-focused applications, including WeChat, SMS, DingTalk, Feishu, and email delivery. It supports unified dispatch design, priority routing, provider-specific message examples, rate limiting, and compliance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Notification provider credentials and webhook URLs could be exposed or misused during implementation.

Mitigation: Store provider credentials in approved secret management, limit access by environment, rotate secrets when needed, and avoid placing webhook URLs or API keys in prompts, logs, or source examples.

Risk: Messages may be sent without required consent, approved templates, or unsubscribe handling.

Mitigation: Record user consent before sends, use provider-approved SMS and WeChat templates, include unsubscribe handling for marketing messages, and review message content before production use.

Risk: High-volume or duplicate sends can violate provider limits, increase cost, or suspend accounts.

Mitigation: Enforce per-user and per-channel rate limits, add idempotency controls, log delivery attempts, and test notification workflows with sandbox accounts before production sends.

Risk: Notifications can disclose sensitive personal data to end users, teams, or third-party channels.

Mitigation: Minimize notification content, avoid full phone numbers or identification data, and route sensitive details to authenticated application views instead of message bodies.

## Reference(s):

- [China Notification Service on ClawHub](https://clawhub.ai/lm203688/skills/china-notification-service)
- [Publisher profile: lm203688](https://clawhub.ai/user/lm203688)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration, API Calls]

**Output Format:** [Markdown with JavaScript examples, workflow guidance, checklists, and reference tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include provider-specific API examples, routing matrices, rate-limit rules, and compliance guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
