## Description:

Dingtalk Message helps agents send and manage DingTalk messages through group webhooks, internal app robots, work notifications, and session webhooks, including Markdown, ActionCard, recall, and read-status workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[breath57](https://clawhub.ai/user/breath57)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send DingTalk group, direct, and work-notification messages from an agent. It also guides recall, read-status checks, webhook replies, credential collection, and channel-specific DingTalk API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored DingTalk app secrets, webhook URLs, access tokens, and agent IDs could be reused to send or recall workplace messages if the config file is exposed.

Mitigation: Treat ~/.dingtalk-skills/config as sensitive, limit local access to the file, and rotate credentials if machine access is shared or uncertain.

Risk: The skill can send broad workplace notifications, including all-user work notifications, when configured with sufficient DingTalk permissions.

Mitigation: Use narrowly scoped DingTalk apps and webhooks, and avoid all-user sends unless the user explicitly requests and confirms that audience.

## Reference(s):

- [DingTalk Message API Reference](references/api.md)
- [ClawHub skill page](https://clawhub.ai/breath57/skills/dingtalk-message)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with shell-script and JSON request examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce curl-based execution scripts and configuration entries for DingTalk credentials, webhooks, access tokens, and agent IDs.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
