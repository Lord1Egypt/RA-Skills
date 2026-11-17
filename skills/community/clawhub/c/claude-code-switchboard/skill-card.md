## Description:

Manage how OpenClaw routes Telegram messages to different Claude model backends. Switch between CLI and API providers with simple config changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josephtandle](https://clawhub.ai/user/josephtandle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and change OpenClaw Telegram routing between Claude CLI backends and API providers, including fallback and restore workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Changing the active model, fallback mode, or restore setting can alter OpenClaw Telegram message routing.

Mitigation: Review the intended routing change before applying it, and confirm the resulting configuration in OpenClaw after the change.

Risk: Restarting the gateway can briefly affect Telegram message processing.

Mitigation: Apply routing changes during an acceptable maintenance window or when a brief interruption is acceptable.

## Reference(s):

- [OpenClaw](https://openclaw.ai)
- [ClawHub skill page](https://clawhub.ai/josephtandle/skills/claude-code-switchboard)
- [Publisher profile](https://clawhub.ai/user/josephtandle)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration guidance]

**Output Format:** [Markdown with inline shell commands and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for OpenClaw routing changes; it does not include executable scripts.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
