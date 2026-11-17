## Description:

Governance behavior for AI agents governed by DashClaw, covering guard checks, approval decisions, action recording, session lifecycle management, and org-specific policy and capability loading from DashClaw MCP resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dashclaw](https://clawhub.ai/user/dashclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and governed agents use this skill to apply DashClaw policy checks, approval waits, audit recording, and session handoff practices during agent work. It is intended for agents operating with the DashClaw MCP server and Mission Control workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DashClaw governance can affect broad agent activity across a working session.

Mitigation: Install it only when the operator intentionally wants DashClaw to govern the session, and verify the MCP server identity, policy provenance, and allowed capability IDs before sensitive work.

Risk: Action records, approvals, and session handoff context may include sensitive, personal, or proprietary information.

Mitigation: Confirm logging destinations, access controls, retention and deletion settings, and redaction rules before using the skill on sensitive work.

## Reference(s):

- [DashClaw Governance Skill Page](https://clawhub.ai/dashclaw/skills/dashclaw-governance)
- [Governance Patterns](references/governance-patterns.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with governance decision tables and tool-call patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DashClaw MCP resources and tools for the full governance flow; includes a static protocol fallback when resources are unavailable.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
