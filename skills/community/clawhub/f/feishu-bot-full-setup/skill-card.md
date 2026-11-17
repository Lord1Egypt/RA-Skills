## Description:

Creates a Feishu enterprise self-built bot and completes permission import, event subscription, card callback setup, and version release.

This skill is ready for commercial/non-commercial use.

## Publisher:

[big-dust](https://clawhub.ai/user/big-dust)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation operators use this skill to create a Feishu enterprise bot through an agent-guided workflow, including QR login, app creation, permission setup, event subscriptions, card callbacks, publishing, and retrieval of app credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automates Feishu developer actions from a logged-in session.

Mitigation: Run it only from an account and tenant authorized to create, configure, and publish Feishu applications, and review the resulting app before broad use.

Risk: The default flow requests many high-impact Feishu permissions.

Mitigation: Review references/permissions.md before use and prefer a reduced, opt-in permission set that matches the bot's actual purpose.

Risk: The generated app_secret may be exposed through chat history or notifications.

Mitigation: Treat app_id and app_secret as credentials, avoid persistent chat disclosure, store them in a secrets manager, and rotate the secret if exposed.

Risk: Runtime setup can modify the Python or system environment and download dependencies.

Mitigation: Run the skill in an isolated environment with pinned dependencies and trusted package and browser download sources.

## Reference(s):

- [Default permissions list](references/permissions.md)
- [Feishu Open Platform](https://open.feishu.cn)
- [ClawHub skill page](https://clawhub.ai/big-dust/skills/feishu-bot-full-setup)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and a final JSON credential object from the create command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The create flow writes a local login QR PNG and returns app_id and app_secret on success.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
