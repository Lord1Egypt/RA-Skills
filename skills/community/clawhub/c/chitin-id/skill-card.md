## Description:

Chitin guides AI agents through creating and maintaining permanent, verifiable identity with ERC-8004 passports, Chitin soul certificates, on-chain certificates, and governance workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eijiac24](https://clawhub.ai/user/eijiac24)

### License/Terms of Use:


## Use Case:

Developers, operators, and AI agents use Chitin to register an agent identity, verify identity status, manage selective disclosure and binding workflows, and interact with related certificate and governance services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration and identity workflows can expose sensitive registration data, prompt-derived fields, API keys, wallet signatures, or private keys if handled carelessly.

Mitigation: Constrain use manually, review which fields become public or permanent, prefer wallet-mediated signing, and never provide owner wallet private keys to MCP tools, SDK helpers, chat transcripts, or unpinned packages.

Risk: MCP server and heartbeat workflows may introduce unreviewed external behavior if agents fetch instructions or run packages without control.

Mitigation: Pin and audit MCP server versions, use reviewed local instructions, and avoid persistent fetch-and-follow heartbeat rules unless the fetched content is controlled and reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/eijiac24/skills/chitin-id)
- [Chitin Documentation](https://chitin.id/docs)
- [Chitin API Base](https://chitin.id/api/v1)
- [Chitin Skill Metadata](https://chitin.id/skill.json)
- [Chitin MCP Documentation](https://chitin.id/docs/mcp)
- [Chitin MCP Server](https://www.npmjs.com/package/chitin-mcp-server)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON examples, shell commands, API request examples, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance can include public identity fields, API endpoints, wallet-mediated signature steps, MCP setup, and recurring heartbeat checks.]

## Skill Version(s):

1.2.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
