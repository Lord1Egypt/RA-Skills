## Description:

Provides a Feishu Open Platform workflow for sending messages, finding group chats and members, uploading message images or files, and preparing Feishu resource-management API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xq-8](https://clawhub.ai/user/xq-8)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to draft Feishu bot messaging workflows, locate chat or member identifiers, and send text, image, or file messages through the Feishu Open Platform API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages, images, or files may be sent to unintended Feishu recipients if identifiers or content are not reviewed.

Mitigation: Confirm recipients, message contents, and exact files before sending through the Feishu bot.

Risk: Feishu APP_ID and APP_SECRET credentials can be exposed through insecure handling or verbose logs.

Mitigation: Keep app credentials secure and avoid debug logging sensitive API responses in production.

Risk: The release describes document creation, but the security guidance warns not to rely on that workflow without additional verification.

Mitigation: Verify or add the document-creation workflow before using the skill for Feishu document operations.

## Reference(s):

- [Feishu Open Platform API Documentation](https://open.feishu.cn/document/server-docs/api-call-guide/server-api-list)
- [ClawHub Skill Page](https://clawhub.ai/xq-8/skills/feishu-messaging-0)

## Skill Output:

**Output Type(s):** [Guidance, Code, API Calls, Configuration]

**Output Format:** [Markdown with Python code examples and Feishu API permission notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu app credentials, bot permissions, recipient identifiers, and file paths before the examples can be used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
