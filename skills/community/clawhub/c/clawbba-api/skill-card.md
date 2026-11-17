## Description:

ClawBBA × OpenClaw connects OpenClaw agents to ClawBBA with one Platform API Key for chat, image, and video model access across web chat, WeChat, Telegram, and other channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawbba-ux](https://clawhub.ai/user/clawbba-ux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure ClawBBA as an OpenAI-compatible provider and guide agents in text chat, image generation, video generation, media recovery, and troubleshooting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags unverified remote installation and persistent OpenClaw runtime changes for manual review.

Mitigation: Install only after trusting the publisher, reviewing the file changes, and preferring a signed or checksum-verified installer with a rollback path.

Risk: The skill stores CLAWBBA_API_KEY locally and modifies OpenClaw configuration.

Mitigation: Use a scoped API key, keep it out of version control, verify local file permissions, and rotate the key if it may have been exposed.

Risk: Repeated media generation after timeouts or incomplete delivery can cause duplicate charges.

Mitigation: Use the documented task recovery and local MEDIA redelivery workflow before regenerating content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawbba-ux/skills/clawbba-api)
- [ClawBBA publisher profile](https://clawhub.ai/user/clawbba-ux)
- [ClawBBA API keys](https://www.clawbba.com/agent/api-keys)
- [ClawBBA API endpoint](https://www.clawbba.com/api/v1)
- [OpenClaw documentation](https://docs.openclaw.ai/)
- [OpenClaw agent behavior](references/openclaw-agent-behavior.md)
- [OpenClaw integration spec](references/openclaw-integration-spec.md)
- [Media capabilities](references/media-capabilities.md)
- [Media dispatch spec](references/media-dispatch-spec.md)
- [Troubleshooting guide](references/SKILL-troubleshooting.md)
- [OpenClaw release manifest](references/openclaw-release-manifest.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration steps, and local media path references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLAWBBA_API_KEY and local OpenClaw configuration; generated media is referenced as local MEDIA paths.]

## Skill Version(s):

2.0.33 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
