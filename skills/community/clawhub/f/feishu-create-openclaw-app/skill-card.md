## Description:

Automates creation and configuration of a Feishu enterprise self-built application for OpenClaw integration through browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diluke1600](https://clawhub.ai/user/diluke1600)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Feishu workspace administrators use this skill to create an OpenClaw integration app, import the required Feishu permissions, and retrieve the app credentials needed for OpenClaw configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad Feishu tenant-level permissions for the new application.

Mitigation: Reduce the imported scope list to the integration's actual needs and have a Feishu administrator review the permissions before approving them.

Risk: The workflow may reveal the Feishu App Secret in chat or logs.

Mitigation: Copy the secret directly into secure configuration or a secret manager, and avoid printing the full secret in agent-visible output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diluke1600/skills/feishu-create-openclaw-app)
- [Feishu developer console](https://open.feishu.cn/app)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration, Text]

**Output Format:** [Markdown with browser automation steps, JSON permission configuration, and credential summary text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive App ID and App Secret values that should be copied into secure configuration storage.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
