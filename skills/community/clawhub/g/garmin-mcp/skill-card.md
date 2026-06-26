## Description: <br>
Connect an MCP-compatible agent to local Garmin Connect sleep, Body Battery, HRV, stress, activities, and training readiness. Use when an AI agent needs setup, usage, safety boundaries, or troubleshooting for Garmin MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidmosiah](https://clawhub.ai/user/davidmosiah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to install, configure, troubleshoot, and verify privacy boundaries for a Garmin MCP server in MCP-compatible clients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Garmin MCP access can expose private wellness data to an authenticated agent. <br>
Mitigation: Run privacy and status checks first, keep user consent explicit, and avoid placing private health data in prompts or logs. <br>
Risk: OAuth tokens or local token files could be exposed during setup or troubleshooting. <br>
Mitigation: Use the local helper/token flow, keep tokens under ~/.garmin-mcp/, and do not print credentials, token files, API keys, or private user data. <br>
Risk: The npm package or linked repository may not match the intended release. <br>
Mitigation: Verify the linked repository and garmin-mcp-unofficial package before installing or running commands. <br>


## Reference(s): <br>
- [Garmin MCP repository](https://github.com/davidmosiah/garminmcp) <br>
- [Garmin connector documentation](https://wellness.delx.ai/connectors/garmin) <br>
- [ClawHub skill page](https://clawhub.ai/davidmosiah/garmin-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include safety, privacy, and troubleshooting guidance for local Garmin MCP setup.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
