## Description:

Coherence Network helps agents browse, rank, and act on ideas, specs, value lineage, contributions, task queues, governance, and federation through the public Coherence Network API, CLI, and MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seeker71](https://clawhub.ai/user/seeker71)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to inspect Coherence Network portfolios, trace contribution and value lineage, manage identities and task queues, and coordinate through governance and federation workflows. It supports read-only API and CLI exploration as well as user-confirmed write actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or change remote Coherence Network records, link identities, interact with task queues, and receive federation messages.

Mitigation: Start with read-only commands, confirm every write or task action with the user, and avoid linking personal or provider identities unless intended.

Risk: The security evidence flags unpinned npm/npx tooling and broad auto-triggering against a public integration.

Mitigation: Review and pin package versions before installing CLI or MCP tooling, and limit automatic execution of inbox or task commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/seeker71/skills/coherence-network)
- [Coherence Network Web](https://coherencycoin.com)
- [Coherence Network API Docs](https://api.coherencycoin.com/docs)
- [Coherence CLI on npm](https://www.npmjs.com/package/coherence-cli)
- [Coherence MCP Server on npm](https://www.npmjs.com/package/coherence-mcp-server)
- [API Endpoint Reference](artifact/references/api-endpoints.md)
- [MCP Server Reference](artifact/references/mcp-server.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with CLI commands, curl examples, endpoint tables, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include write-operation instructions that require user confirmation and optional environment variables for API URL and keys.]

## Skill Version(s):

0.11.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
