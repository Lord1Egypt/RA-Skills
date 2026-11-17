## Description:

ByteHouse slow-query analysis and performance optimization skill for identifying slow queries, reviewing query performance, inspecting execution plans, and analyzing query history trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to inspect ByteHouse slow-query behavior, summarize recent query-log statistics, and generate optimization guidance for performance tuning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run remote MCP server code from a mutable branch.

Mitigation: Use a pinned or preinstalled trusted MCP server before running the analysis.

Risk: The runtime passes environment variables to the MCP subprocess.

Mitigation: Run in a restricted environment with read-only ByteHouse credentials and remove unrelated secrets from the environment.

Risk: Generated slow-query reports may contain sensitive query text, identifiers, and operational metrics.

Mitigation: Protect generated output files and delete them when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-bytehouse-slow-query)
- [Volcengine ByteHouse MCP server runtime dependency](https://github.com/volcengine/mcp-server@main#subdirectory=server/mcp_server_bytehouse)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown usage guidance with shell commands and generated JSON analysis files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save slow-query analysis, query statistics, and optimization suggestion files under an output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
