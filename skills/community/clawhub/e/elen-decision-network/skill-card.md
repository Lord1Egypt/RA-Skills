## Description: <br>
Teaches agents how to query, expand, and cleanly commit technical, design, and product constraints to the Elen SQLite decision graph via the Elen Context Server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NicoIzco](https://clawhub.ai/user/NicoIzco) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to consult and update a local Elen decision graph before making technical, design, security, or product changes, preserving visible reasoning and constraints across work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to run a pinned npm MCP package. <br>
Mitigation: Verify trust in the @learningnodes/elen-mcp package and publisher before installing or enabling the MCP server. <br>
Risk: The decision graph can become persistent memory for sensitive technical, product, or business reasoning. <br>
Mitigation: Avoid committing secrets, credentials, or confidential business details unless the MCP server's storage and sharing behavior has been reviewed. <br>
Risk: Agent behavior depends on a locally configured MCP server and its returned decision context. <br>
Mitigation: Confirm the Elen server configuration and review important suggested or committed decisions before using them to guide broad codebase changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NicoIzco/elen-decision-network) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands] <br>
**Output Format:** [Markdown with JSON configuration examples and MCP tool guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference MCP tool calls for querying, committing, and superseding decision graph entries.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
