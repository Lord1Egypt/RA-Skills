## Description:

Send Markdown-formatted messages with message type labels and @mentions to DingTalk group chats through a bot webhook with optional signature verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrewqumm](https://clawhub.ai/user/andrewqumm)

### License/Terms of Use:


## Use Case:

Developers and automation operators use this skill to send task results, alerts, and operational notifications to DingTalk group chat robots. It supports direct CLI use and programmatic calls from other agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured webhooks can redirect selected message content to arbitrary or non-HTTPS endpoints.

Mitigation: Require HTTPS DingTalk webhook URLs, store webhook and signing secrets as protected secrets, and review configuration before installation.

Risk: Notification content and @all mentions can expose sensitive information or over-notify a DingTalk group.

Mitigation: Review message content before sending sensitive data, avoid shared .dingtalk-push.json files, and require deliberate use of @all.

## Reference(s):

- [ClawHub DingTalk Push page](https://clawhub.ai/andrewqumm/skills/dingtalk-push)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown messages sent to DingTalk with JSON send results and optional command-line status output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports message type, title, mobile-number mentions, @all, webhook configuration, and an optional signing secret.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
