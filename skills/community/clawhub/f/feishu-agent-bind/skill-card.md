## Description:

Bind a Feishu group chat to a specific OpenClaw agent for dedicated routing, workspace setup, binding configuration, session cleanup, and gateway restart.

This skill is ready for commercial/non-commercial use.

## Publisher:

[embracex1998](https://clawhub.ai/user/embracex1998)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to route a Feishu group chat to a dedicated OpenClaw agent with an isolated workspace. It guides configuration updates, stale session cleanup, gateway restart, and verification for group-to-agent routing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configuration edits can rewrite core OpenClaw routing and workspace settings.

Mitigation: Back up OpenClaw configuration, validate exact agent, chat, and account identifiers, and prefer official OpenClaw configuration commands where available.

Risk: The session cleanup snippet can delete session data too broadly if placeholders or matching keys are wrong.

Mitigation: Do not run deletion commands until matching files and keys have been reviewed, narrowed to the intended chat, and confirmed restorable from backup.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline bash, Python, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires exact OpenClaw agent IDs, Feishu chat IDs, and Feishu account IDs before applying configuration changes.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
