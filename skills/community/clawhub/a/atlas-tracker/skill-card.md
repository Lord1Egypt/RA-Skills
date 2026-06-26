## Description: <br>
Work with Atlas Tracker mindmaps through MCP and OpenClaw tools for reading, creating, updating, attaching files to, and commenting on map nodes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DIdro](https://clawhub.ai/user/DIdro) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Atlas Tracker users can use this skill to navigate Atlas Tracker map structure, create and update branches, manage typed node properties, add link nodes, upload files, and work with node comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Atlas Tracker service trust and access to Atlas Tracker credentials and data. <br>
Mitigation: Use trusted Atlas Tracker and RedForester service access, keep credentials out of chat and shell history, and prefer configured MCP tools over raw curl or ad hoc API calls. <br>
Risk: The skill can upload arbitrary local files to Atlas Tracker nodes. <br>
Mitigation: Require explicit confirmation of the exact local file path and target node before upload. <br>
Risk: Persistent local service setup and direct API use can expose data if configured too broadly. <br>
Mitigation: Review the local MCP server configuration, API key scope, and target Atlas Tracker account before enabling write operations. <br>


## Reference(s): <br>
- [Atlas Tracker skill page](https://clawhub.ai/DIdro/atlas-tracker) <br>
- [Atlas Tracker](https://app.redforester.com) <br>
- [Atlas Tracker REST API Patterns](references/api-patterns.md) <br>
- [Atlas Tracker Node Types Guide](references/node-types-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, text] <br>
**Output Format:** [Markdown guidance with inline commands, JSON examples, and MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local file paths, Atlas Tracker node URLs, credentials configured outside chat, and MCP tool responses.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
