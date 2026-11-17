## Description:

OpenClaw skill for Discord Bot API workflows, covering interactions, commands, messages, and operations using direct HTTPS requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ingejanben268](https://clawhub.ai/user/ingejanben268)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to plan Discord bot workflows, command UX, interaction handling, REST requests, and operational checklists for bot deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled scripts load a local .env file as shell code.

Mitigation: Review the skill directory and .env contents before running scripts, and avoid executing files from untrusted sources.

Risk: The bundled webhook script sends message text to the configured Discord webhook URL.

Mitigation: Verify WEBHOOK_URL points to the intended Discord webhook before use, and do not send secrets or private data as message text.

Risk: Server security evidence marks the release as suspicious because executable shell scripts are under-documented.

Mitigation: Treat the documentation as a general Discord API guide and run scripts only after manual review.

## Reference(s):

- [Discord API Overview](references/discord-api-overview.md)
- [Auth and Tokens](references/discord-auth-and-tokens.md)
- [Interactions](references/discord-interactions.md)
- [Application Commands](references/discord-app-commands.md)
- [Messages and Components](references/discord-messages-components.md)
- [Gateway vs Webhooks](references/discord-gateway-webhooks.md)
- [Rate Limits and Reliability](references/discord-rate-limits.md)
- [HTTP Request Templates](references/discord-request-templates.md)
- [Discord Bot Feature Map](references/discord-feature-map.md)
- [Discord API](https://discord.com/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with request examples, shell command snippets, and operational checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
