## Description: <br>
Connect to Civic Nexus MCP for 100+ integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[civictechuser](https://clawhub.ai/user/civictechuser) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to connect an agent to Civic Nexus MCP integrations, then list, search, inspect schemas, and call tools across connected services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad access to many connected services through Civic Nexus. <br>
Mitigation: Use a least-privilege Nexus token and profile, connect only required services, and require manual approval before write, delete, send, bulk, or SQL-execution actions. <br>
Risk: NEXUS_TOKEN can grant access to connected services if exposed. <br>
Mitigation: Store the token only in environment or secret configuration, avoid pasting it into prompts or logs, and rotate it after suspected exposure. <br>
Risk: Some tool calls may trigger OAuth authorization or long-running continuation flows. <br>
Mitigation: Show authorization URLs to the user, confirm the requested service and action, and continue only after user authorization. <br>


## Reference(s): <br>
- [Civic Nexus Documentation](https://docs.civic.com) <br>
- [Civic Nexus](https://nexus.civic.com) <br>
- [Civic Nexus MCP Endpoint](https://nexus.civic.com/hub/mcp) <br>
- [ClawHub Skill Page](https://clawhub.ai/civictechuser/civic-nexus-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NEXUS_URL and NEXUS_TOKEN, plus either mcporter or npx.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
