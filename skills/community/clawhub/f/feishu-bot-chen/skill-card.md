## Description:

Feishu (Lark) Bot integration for messaging, group management, and approval workflows. Send messages, manage groups, handle approvals, and automate notifications via Feishu Open Platform API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason-aka-chen](https://clawhub.ai/user/jason-aka-chen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to automate Feishu/Lark messaging, group administration, approval workflows, contact lookups, and file or image delivery through the Feishu Open Platform API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook sends can transmit caller-supplied content to arbitrary URLs.

Mitigation: Expose webhook sending only to trusted workflows, require an allowlist of approved Feishu/Lark webhook URLs, and request user confirmation before sending sensitive content.

Risk: Messages, approval forms, group membership, and contact data may contain sensitive business information.

Mitigation: Limit use to approved Feishu destinations, minimize message content, and treat returned Feishu API data as sensitive.

Risk: Authenticated API calls can send messages, manage groups, and create or cancel approvals using app credentials.

Mitigation: Store FEISHU_APP_ID and FEISHU_APP_SECRET securely, grant only required Feishu permissions, and run the skill in trusted agent workflows.

## Reference(s):

- [Feishu Open Platform](https://open.feishu.cn)
- [Feishu App Console](https://open.feishu.cn/app)
- [Feishu API Documentation](https://open.feishu.cn/document)
- [Feishu Bot Development Guide](https://open.feishu.cn/document/home/introduction-to-feishu-platform/bot-development-odyssey)
- [ClawHub Skill Page](https://clawhub.ai/jason-aka-chen/skills/feishu-bot-chen)
- [ClawHub Publisher Profile](https://clawhub.ai/user/jason-aka-chen)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples, shell configuration commands, and JSON-like API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FEISHU_APP_ID and FEISHU_APP_SECRET for authenticated Feishu Open Platform API calls.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
