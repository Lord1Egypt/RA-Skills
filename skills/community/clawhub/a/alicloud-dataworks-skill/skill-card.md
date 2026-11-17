## Description:

Manage Alibaba Cloud DataWorks via OpenAPI/MCP Server. Use for data development, workflow operations, data quality, metadata lineage, workspace management, and troubleshooting across the entire DataWorks platform through a single skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samuelhsin](https://clawhub.ai/user/samuelhsin)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers, data engineers, and operators use this skill to discover Alibaba Cloud DataWorks APIs, configure MCP access, manage DataWorks projects and workflows, inspect metadata and lineage, and perform data quality or operations tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Alibaba Cloud DataWorks control through cloud access keys can affect projects, workflows, metadata, quality rules, and operations state.

Mitigation: Use a dedicated least-privilege Alibaba Cloud RAM identity, prefer temporary credentials, and require explicit confirmation for state-changing or privilege-affecting API calls.

Risk: The MCP server package is referenced without a pinned version and can dynamically expose a broad DataWorks API surface.

Mitigation: Pin and review the MCP server package version, restrict TOOL_NAMES or TOOL_CATEGORIES to the task, and review available tools before use.

Risk: Access keys may be exposed if copied into committed configuration or logs.

Mitigation: Provide credentials through environment variables or a secure credential store and avoid committing access keys.

## Reference(s):

- [MCP Server integration](references/mcp_server.md)
- [Sources](references/sources.md)
- [DataWorks OpenAPI product page](https://api.aliyun.com/product/dataworks-public)
- [DataWorks OpenAPI metadata](https://next.api.aliyun.com/meta/v1/products/dataworks-public/versions/2024-05-18/api-docs.json)
- [DataWorks MCP tools discovery](https://dataworks.data.aliyun.com/pop-mcp-tools)
- [Alibaba Cloud DataWorks documentation](https://www.alibabacloud.com/help/dataworks)
- [DataWorks MCP usage guide](https://www.alibabacloud.com/help/dataworks/user-guide/dataworks-mcp-server-function-usage)
- [DataWorks MCP server package](https://www.npmjs.com/package/alibabacloud-dataworks-mcp-server)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API inventory files under output/alicloud-dataworks/ when the included metadata discovery script is run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
