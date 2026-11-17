## Description:

Connects a Feishu bot by using the Feishu app registration flow to generate a user setup link, poll for client credentials after user confirmation, and continue the OpenClaw pairing flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wt865143010](https://clawhub.ai/user/wt865143010)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to connect or bind a Feishu bot through a direct setup link, then continue gateway configuration and pairing after Feishu returns the app credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may obtain and use Feishu App ID and App Secret during setup.

Mitigation: Treat the client_secret as sensitive, avoid sharing it in chat where possible, and prefer local credential storage or redaction from logs.

## Reference(s):

- [ClawHub skill release: Feishu Connect 1.0.0](https://clawhub.ai/wt865143010/skills/feishu-connect-1-0-0)
- [Feishu app registration endpoint](https://accounts.feishu.cn/oauth/v1/app/registration)
- [Feishu OpenClaw setup page](https://open.feishu.cn/page/openclaw?user_code=XXXX-XXXX&from=maxclaw)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash commands and plain setup links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Feishu setup URLs, user codes, and follow-up pairing instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
