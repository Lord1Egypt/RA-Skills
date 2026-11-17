## Description:

Automates creation and configuration of Feishu bots, including app creation, permission setup, webhook configuration, and local configuration output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[839305939wang](https://clawhub.ai/user/839305939wang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Feishu workspace administrators use this skill to create Feishu bot applications, assign requested permissions, configure webhooks, and generate the bot configuration needed for follow-on automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Feishu tenant credentials, generated app secrets, access tokens, and webhook data that could be exposed through logs or saved configuration files.

Mitigation: Run it only in a trusted terminal, avoid environments where stdout is centrally logged, choose a private output path, restrict access to the generated config file, and do not commit generated credentials.

Risk: Changing FEISHU_API_BASE can send Feishu credentials and tokens to a nonstandard endpoint.

Mitigation: Keep the default Feishu API base unless the alternate endpoint is explicitly trusted and controlled.

Risk: Requested bot permissions can grant access to messaging, chat, contacts, calendar, or drive data.

Mitigation: Request the minimum required permission set and review tenant approval requirements before enabling the bot.

## Reference(s):

- [Feishu Open Platform](https://open.feishu.cn)
- [ClawHub skill page](https://clawhub.ai/839305939wang/skills/feishu-bot-creator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in a local JSON configuration file containing Feishu app credentials, webhook data, and selected permissions.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md metadata.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
