## Description: <br>
Teach the agent how to connect the published CortexPilot read-only MCP package, choose the right public lane, and use the stable read-only tools without overclaiming hosted or write-capable support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaojiou176](https://clawhub.ai/user/xiaojiou176) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect CortexPilot's published read-only MCP package to OpenHands or OpenClaw and choose the right inspection lane for runs, workflows, queues, approvals, proof summaries, or incidents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install path runs a third-party PyPI package through uvx. <br>
Mitigation: Install only when the publisher and package version are trusted, and review the package before use in sensitive environments. <br>
Risk: Users may expect hosted or write-capable CortexPilot behavior that this skill does not provide. <br>
Mitigation: Keep usage to the documented read-only MCP tools and avoid credentials unless a separate, clearly scoped workflow requires them. <br>


## Reference(s): <br>
- [CortexPilot Adoption Router on ClawHub](https://clawhub.ai/xiaojiou176/cortexpilot-adoption-router) <br>
- [Install The Published CortexPilot MCP](references/INSTALL.md) <br>
- [CortexPilot MCP Capabilities](references/CAPABILITIES.md) <br>
- [OpenHands / OpenClaw Demo Walkthrough](references/DEMO.md) <br>
- [CortexPilot Troubleshooting](references/TROUBLESHOOTING.md) <br>
- [CortexPilot MCP Tool Map](references/tool-map.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Keeps responses short and operational: chosen lane, next actions, boundary reminder, and one exact MCP tool or install snippet.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and manifest.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
