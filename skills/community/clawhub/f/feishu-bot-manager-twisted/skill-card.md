## Description:

Configures and manages multiple Feishu bot accounts for OpenClaw, including account-level or group-chat message routing to selected agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twistedcz](https://clawhub.ai/user/twistedcz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to add Feishu bot credentials, configure account-level or group-chat routing to agents, and restart the gateway after configuration updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify live OpenClaw Feishu configuration.

Mitigation: Run it only when intending to update the active Feishu setup, review the generated ~/.openclaw/openclaw.json, and keep the automatic backup available for rollback.

Risk: Feishu App Secrets may be exposed through command-line history or configuration review workflows.

Mitigation: Avoid placing real App Secrets directly in shell history and restrict access to generated configuration files and backups.

Risk: The default open direct-message policy and wildcard allowlist can expose the bound agent to untrusted Feishu users.

Mitigation: Prefer pairing or allowlist access, and confirm the bound agent does not expose sensitive tools or data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/twistedcz/skills/feishu-bot-manager-twisted)
- [ClawHub publisher profile](https://clawhub.ai/user/twistedcz)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command-line examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify OpenClaw Feishu configuration, create a backup, and restart the OpenClaw Gateway when executed.]

## Skill Version(s):

0.0.1 (source: evidence release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
