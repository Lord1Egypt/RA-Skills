## Description: <br>
Teach the agent how to connect the published DealWatch MCP package, choose the right read-only tool, and guide the user through the compare-first safe path without claiming hosted or write-capable features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaojiou176](https://clawhub.ai/user/xiaojiou176) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect a local DealWatch MCP server in OpenHands or OpenClaw, check runtime readiness, and choose read-only comparison, watch, or diagnostic tools without creating durable state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP server is installed from a pinned PyPI package and added to a host MCP configuration. <br>
Mitigation: Confirm that dealwatch==1.0.1 is the intended trusted package before installing or adding it to OpenHands or OpenClaw. <br>
Risk: Users may assume the skill supports write-capable, hosted, marketplace, or autonomous recommendation workflows. <br>
Mitigation: Keep use to the documented local-first read-only tools, start with runtime readiness or compare preview, and state the boundary when answering. <br>


## Reference(s): <br>
- [DealWatch Read-only Builder ClawHub listing](https://clawhub.ai/xiaojiou176/dealwatch-readonly-builder) <br>
- [Install The Published DealWatch MCP](references/INSTALL.md) <br>
- [DealWatch MCP Capabilities](references/CAPABILITIES.md) <br>
- [OpenHands / OpenClaw Demo Walkthrough](references/DEMO.md) <br>
- [DealWatch Troubleshooting](references/TROUBLESHOOTING.md) <br>
- [OpenHands MCP configuration](references/OPENHANDS_MCP_CONFIG.json) <br>
- [OpenClaw MCP configuration](references/OPENCLAW_MCP_CONFIG.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only workflow guidance; no durable state creation.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence and manifest.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
