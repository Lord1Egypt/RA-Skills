## Description: <br>
Control Assimilate Live FX / SCRATCH - professional color grading, compositing, and virtual production software - via MCP with 88 tools across 14 categories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ergopooka](https://clawhub.ai/user/ergopooka) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and post-production operators use this skill to let an AI assistant operate Assimilate Live FX or SCRATCH through MCP for project navigation, media import, grading, playback, snapshots, output setup, and rendering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an assistant change project state, modify grades, import files, create outputs, or start renders in Assimilate Live FX/SCRATCH. <br>
Mitigation: Require explicit user confirmation before state-changing, file-import, grading, output, or render actions. <br>
Risk: A reachable HTTP server or exposed authorization key could allow unwanted control of the connected Assimilate environment. <br>
Mitigation: Keep the HTTP server bound to localhost where possible, protect any authorization key, and use SSH tunnels only to trusted hosts. <br>
Risk: Installing and running the MCP server executes the third-party assimilate-mcp npm package. <br>
Mitigation: Install only when the publisher and npm package are trusted for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ergopooka/assimilate-mcp) <br>
- [Assimilate MCP npm package](https://www.npmjs.com/package/assimilate-mcp) <br>
- [Assimilate REST API](https://github.com/Assimilate-Inc/Assimilate-REST) <br>
- [Assimilate Inc](https://assimilateinc.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces MCP setup and operational guidance for an assistant that calls Assimilate Live FX/SCRATCH tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
