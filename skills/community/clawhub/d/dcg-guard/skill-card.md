## Description:

Hard-blocks dangerous shell commands before execution via OpenClaw's before_tool_call plugin hook, using built-in rules with optional DCG binary fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[starensen](https://clawhub.ai/user/starensen)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to add a gateway-level command guard that blocks destructive shell commands before an OpenClaw agent can execute them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer downloads and runs unpinned remote code.

Mitigation: Review the upstream source before installation and prefer a pinned release with checksum verification.

Risk: The plugin has persistent gateway access and may log full blocked commands.

Mitigation: Install only in trusted OpenClaw environments and treat command logs as potentially sensitive.

Risk: The guard can fail open if the DCG binary is missing or crashes.

Mitigation: Do not rely on it as the only safety control; keep human review and operational policy for destructive commands.

## Reference(s):

- [DCG Guard ClawHub listing](https://clawhub.ai/starensen/skills/dcg-guard)
- [Destructive Command Guard repository](https://github.com/Dicklesworthstone/destructive_command_guard)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit block messages that include the blocked command and matched rule; safe commands pass through silently.]

## Skill Version(s):

1.1.0 (source: server release metadata, package.json, openclaw.plugin.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
