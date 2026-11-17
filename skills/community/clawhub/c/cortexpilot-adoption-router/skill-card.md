## Description:

Teach the agent how to connect the published CortexPilot read-only MCP package, choose the right public lane, and use the stable read-only tools without overclaiming hosted or write-capable support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaojiou176](https://clawhub.ai/user/xiaojiou176)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect CortexPilot's published read-only MCP server to OpenHands or OpenClaw, then choose the right inspection lane for runs, workflows, queues, approvals, proof summaries, compare summaries, and incident summaries. The skill helps keep agent responses within the documented read-only boundary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to launch a pinned external PyPI package as a local MCP server.

Mitigation: Review and trust cortexpilot-orchestrator==0.1.0a4 before enabling it, prefer a sandboxed host environment, and avoid exposing unrelated credentials or private files to the MCP process.

Risk: Users may ask the agent to mutate CortexPilot state or rely on hosted/write-capable behavior that this release does not provide.

Mitigation: Keep responses on the documented read-only inspection lane and explicitly remind users when a requested hosted or write-capable surface is outside the artifact boundary.

## Reference(s):

- [CortexPilot Adoption Router on ClawHub](https://clawhub.ai/xiaojiou176/skills/cortexpilot-adoption-router)
- [OpenHands Extensions Pull Request 151](https://github.com/OpenHands/extensions/pull/151)
- [Install The Published CortexPilot MCP](references/INSTALL.md)
- [CortexPilot MCP Capabilities](references/CAPABILITIES.md)
- [OpenHands / OpenClaw Demo Walkthrough](references/DEMO.md)
- [CortexPilot Troubleshooting](references/TROUBLESHOOTING.md)
- [CortexPilot MCP Tool Map](references/tool-map.md)
- [OpenHands MCP Config](references/OPENHANDS_MCP_CONFIG.json)
- [OpenClaw MCP Config](references/OPENCLAW_MCP_CONFIG.json)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Short operational responses naming the chosen lane, next actions, one boundary reminder, and one exact MCP tool or install snippet.]

## Skill Version(s):

1.1.1 (source: server release evidence and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
