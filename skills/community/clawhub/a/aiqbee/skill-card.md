## Description: <br>
Connect to your Aiqbee knowledge graph via MCP. Search, create, and link neurons across your architecture, portfolio, and digital strategy brains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[louisgoodier](https://clawhub.ai/user/louisgoodier) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and teams use this skill to connect an assistant to an Aiqbee knowledge graph for searching, creating, updating, deleting, and linking knowledge records across architecture, portfolio, and digital strategy workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent connected through this skill can change or delete Aiqbee business knowledge-graph records through the signed-in account. <br>
Mitigation: Use the skill only with an Aiqbee account or workspace where agent write access is acceptable, and explicitly confirm update and delete requests before execution. <br>
Risk: OAuth sign-in and MCP endpoint use could expose the user to an unintended destination if not checked. <br>
Mitigation: Verify the OAuth destination and MCP endpoint before signing in. <br>


## Reference(s): <br>
- [Aiqbee Platform](https://aiqbee.com) <br>
- [Aiqbee App](https://app.aiqbee.com) <br>
- [Aiqbee Documentation](https://app.aiqbee.com/help) <br>
- [Aiqbee MCP Server](https://mcp.aiqbee.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Configures an MCP connection that can issue read and write tool calls after OAuth sign-in.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
