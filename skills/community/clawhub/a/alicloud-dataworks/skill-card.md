## Description:

Operate Alibaba Cloud DataWorks through dynamic API discovery and official SDKs for Node.js, Python, and Java across data development, workflow operations, data integration, data quality, metadata lineage, workspace management, and related DataWorks APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samuelhsin](https://clawhub.ai/user/samuelhsin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data platform operators use this skill to discover and call Alibaba Cloud DataWorks OpenAPI operations for data development, operations, data quality, metadata lineage, and workspace administration. It helps agents select APIs, prepare SDK or MCP-based calls, and verify results with describe, list, and get operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to use Alibaba Cloud credentials for broad DataWorks administrative actions.

Mitigation: Use a dedicated least-privilege RAM identity, avoid personal or root keys, and confirm destructive actions before execution.

Risk: The MCP server package and dynamically fetched tool metadata may change outside the skill release.

Mitigation: Pin and review the MCP server package, prefer local vetted tool metadata when available, and restrict tool categories or names to the task.

Risk: Generated API metadata may be less trustworthy when TLS fallback behavior is used by discovery scripts.

Mitigation: Treat generated API metadata cautiously until TLS fallback behavior is fixed, and verify important parameters against official documentation or SDK references.

## Reference(s):

- [MCP Server integration](artifact/references/mcp_server.md)
- [Sources](artifact/references/sources.md)
- [DataWorks documentation](https://www.alibabacloud.com/help/dataworks)
- [OpenAPI Explorer](https://api.aliyun.com/product/dataworks-public)
- [DataWorks OpenAPI metadata](https://next.api.aliyun.com/meta/v1/products/dataworks-public/versions/2024-05-18/api-docs.json)
- [DataWorks MCP Server package](https://www.npmjs.com/package/alibabacloud-dataworks-mcp-server)
- [DataWorks MCP Server source](https://github.com/aliyun/alibabacloud-dataworks-mcp-server)
- [Alibaba Cloud Java SDK source](https://github.com/aliyun/alibabacloud-java-sdk/tree/master/dataworks-public-20240518)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with inline code, shell commands, SDK snippets, configuration examples, and API request details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce DataWorks SDK call examples, MCP server configuration, API discovery commands, and verification steps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
