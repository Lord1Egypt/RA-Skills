## Description:

Analyzes ByteHouse database metadata through a ByteHouse MCP server to generate schema, data asset catalog, and table lineage outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to inspect ByteHouse table structure, generate a data asset catalog, and identify basic lineage relationships across tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs remotely sourced ByteHouse MCP code with the user's environment.

Mitigation: Use an isolated environment, allow only required environment variables, and prefer a version pinned to a reviewed commit before production use.

Risk: Generated schema, catalog, and lineage files may persist sensitive database metadata.

Mitigation: Use a least-privilege read-only ByteHouse account, write only to an approved output directory, and review or redact outputs before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-bytehouse-data-asset-analyzer)
- [ByteHouse MCP server dependency](https://github.com/volcengine/mcp-server/tree/main/server/mcp_server_bytehouse)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance, json files]

**Output Format:** [Markdown guidance with bash and Python snippets, plus generated schema, catalog, and lineage JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated metadata files may contain database schema, table, column, engine, tag, and lineage details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
