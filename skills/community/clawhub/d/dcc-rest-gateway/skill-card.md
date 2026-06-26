## Description: <br>
Controls live DCC hosts such as Maya, Blender, Houdini, Photoshop, and 3ds Max through the DCC-MCP gateway REST API without requiring an MCP client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loonghao](https://clawhub.ai/user/loonghao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical artists use this skill to inventory registered DCC instances, discover REST-exposed tools, inspect schemas, and make approved API calls through a local DCC-MCP gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent REST calls can modify DCC scenes or files through the local gateway. <br>
Mitigation: Review tool schemas before calls and require explicit approval for actions that can modify scenes, files, adapters, GUI applications, or persistent configuration. <br>
Risk: Gateway setup or zero-instance troubleshooting can lead to installation, GUI launch, or environment changes. <br>
Mitigation: Follow the consent-first setup flow and do not run install commands, launch GUI applications, or change environment or configuration files without user approval. <br>
Risk: DCC restarts can invalidate instance IDs and tool slugs. <br>
Mitigation: Re-run instance inventory after crashes or restarts and use freshly discovered tool slugs from search results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/loonghao/dcc-rest-gateway) <br>
- [DCC REST Gateway homepage](https://github.com/loonghao/dcc-mcp-core/blob/main/skills/dcc-rest-gateway/SKILL.md) <br>
- [REST API surface](https://github.com/loonghao/dcc-mcp-core/blob/main/docs/guide/rest-api-surface.md) <br>
- [REST cheatsheet](references/REST_CHEATSHEET.md) <br>
- [Zero instances setup guide](references/ZERO_INSTANCES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with inline shell and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a reachable DCC-MCP gateway URL and curl or Python for health checks.] <br>

## Skill Version(s): <br>
0.17.40 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
