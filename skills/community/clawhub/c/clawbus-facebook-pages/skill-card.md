## Description:

Publish and manage Facebook Page posts, media, comments, feeds, and insights through a preconfigured MyBrandMetrics API connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawbus](https://clawhub.ai/user/clawbus)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect Facebook Pages through MyBrandMetrics, publish Page content, moderate comments, read feeds, and retrieve Page or post insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles powerful Facebook Pages publishing credentials and can publish, edit, hide, unhide, or delete Page content.

Mitigation: Use least-privileged or test credentials and require explicit confirmation of the target Page, content, IDs, and intended visibility before write or moderation actions.

Risk: Credentials can be sent to an unintended API host if config.json, MBM_BASE_URL, or --base-url is set incorrectly.

Mitigation: Verify config.json and any base URL override before use, and prefer the default MyBrandMetrics HTTPS API host.

## Reference(s):

- [Configuration](references/configuration.md)
- [Examples](references/examples.md)
- [Clawbus](https://www.clawbus.com/)
- [MyBrandMetrics](https://mybrandmetrics.com/)
- [MyBrandMetrics API Host](https://api.mybrandmetrics.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and structured JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MyBrandMetrics credentials and Facebook Page, account, connection, post, object, or comment identifiers depending on the workflow.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
