## Description:

Create and wire a new OpenClaw agent with a fixed workflow for Feishu routing, OpenClaw channel accounts, bindings, session.dmScope, gateway restart, and binding verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meichuanyi](https://clawhub.ai/user/meichuanyi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create a new OpenClaw agent for Feishu and update the routing configuration for either a dedicated bot account or a peer-based group/direct route.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently modify OpenClaw Feishu routing configuration and restart the gateway.

Mitigation: Verify agent_id, account_id, peer_id, and dmScope before applying changes; use dry-run behavior where possible and schedule gateway restarts for a safe window.

Risk: Feishu app secrets and routing identifiers can appear in command arguments, output, logs, or configuration backups.

Mitigation: Avoid exposing app secrets in shared command transcripts, redact sensitive output, and protect backup files that may contain credentials.

## Reference(s):

- [OpenClaw Agent Creator ClawHub Page](https://clawhub.ai/meichuanyi/skills/feishu-agent-skills)
- [Routing Modes Reference](artifact/references/routing-modes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with shell commands and JSON configuration summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces concise change summaries and verification results after OpenClaw configuration updates.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/SKILL.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
