## Description:

Teach the agent how to connect the published DealWatch MCP package, choose the right read-only tool, and guide the user through the compare-first safe path without claiming hosted or write-capable features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaojiou176](https://clawhub.ai/user/xiaojiou176)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect DealWatch to OpenHands or OpenClaw, confirm local runtime readiness, and choose read-only MCP tools for grocery URL comparison or watch-state inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to run a pinned external MCP package from PyPI.

Mitigation: Install only when the user intends to use DealWatch; stricter environments should review the package source and dependencies and run it in a constrained environment.

Risk: A misconfigured or unhealthy local DealWatch runtime can make read-only compare workflows fail or produce incomplete guidance.

Mitigation: Start with get_runtime_readiness and stop to report runtime problems before attempting compare_preview.

Risk: Users may assume the skill supports hosted, write-capable, marketplace, or autonomous recommendation features.

Mitigation: Keep responses inside the documented local-first read-only boundary and avoid claims about unsupported hosted or write-side capabilities.

## Reference(s):

- [Install The Published DealWatch MCP](references/INSTALL.md)
- [DealWatch MCP Capabilities](references/CAPABILITIES.md)
- [OpenHands / OpenClaw Demo Walkthrough](references/DEMO.md)
- [DealWatch Troubleshooting](references/TROUBLESHOOTING.md)
- [DealWatch MCP Tool Map](references/tool-map.md)
- [OpenHands MCP Config](references/OPENHANDS_MCP_CONFIG.json)
- [OpenClaw MCP Config](references/OPENCLAW_MCP_CONFIG.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only operational guidance; does not create durable DealWatch state.]

## Skill Version(s):

1.1.1 (source: server release evidence and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
