## Description:

This skill should be used when users need to send notifications to Feishu (Lark) via webhook. It supports multiple message types including text, rich text, interactive cards, and images. Users must configure webhook URLs in ~/.openclaw/skills/feishu-notify/config.json before using this skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alex098929](https://clawhub.ai/user/alex098929)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send Feishu or Lark group notifications, alerts, task updates, rich text posts, interactive cards, and image messages through configured webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages may be posted externally to Feishu without confirmed approval.

Mitigation: Require manual approval before sending, and review the target webhook, destination, and message content before execution.

Risk: Webhook URLs are secrets and anyone with a valid URL can send messages to the target chat.

Mitigation: Use only trusted Feishu webhook URLs, do not commit config.json, restrict local file permissions, and rotate webhooks when exposure is suspected.

Risk: Security evidence reports under-scoped controls around webhook destinations and template files.

Mitigation: Use allowlisted webhook names and predefined templates, and harden or avoid custom template paths until destination and template controls are reviewed.

## Reference(s):

- [Feishu Webhook API Documentation](artifact/references/api_documentation.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance, shell commands, JSON message payloads, and text delivery status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can send external Feishu webhook POST requests using user-configured webhook URLs.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
