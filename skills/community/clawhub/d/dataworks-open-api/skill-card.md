## Description:

Operate Alibaba Cloud DataWorks through dynamic API discovery and official SDKs for data development, workflow operations, data integration, data quality, metadata lineage, and workspace administration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samuelhsin](https://clawhub.ai/user/samuelhsin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to discover and call Alibaba Cloud DataWorks Open APIs, generate SDK-based requests, configure MCP access, and troubleshoot DataWorks project, workflow, quality, metadata, and workspace operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to use broad Alibaba Cloud credentials for DataWorks operations.

Mitigation: Use short-lived or least-privilege RAM/STS credentials, prefer a credentials URI where appropriate, and avoid storing static keys in shell history or shared configuration.

Risk: SDK and MCP package installation examples do not pin package versions.

Mitigation: Pin SDK and MCP package versions during deployment and review package provenance before installation.

Risk: Helper scripts may generate API metadata from documentation or metadata endpoints whose TLS verification behavior has been flagged by security evidence.

Mitigation: Do not rely on generated API metadata unless TLS verification is fixed or the fetched source is independently verified.

Risk: MCP tool exposure can be broader than a user task requires.

Mitigation: Restrict MCP access with TOOL_NAMES or TOOL_CATEGORIES and avoid NODE_ENV=development unless pre-release tool definitions are intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samuelhsin/skills/dataworks-open-api)
- [ClawHub source homepage](https://github.com/aliyun/alibabacloud-bigdata-skills/tree/main/skills/dataworks/open-api)
- [Cookbook](references/cookbook.md)
- [MCP Server Integration](references/mcp_server.md)
- [Sources](references/sources.md)
- [DataWorks documentation](https://www.alibabacloud.com/help/dataworks)
- [OpenAPI Explorer](https://api.aliyun.com/product/dataworks-public)
- [DataWorks MCP Server package](https://www.npmjs.com/package/alibabacloud-dataworks-mcp-server)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with inline code, shell commands, API request examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Alibaba Cloud SDK calls, MCP configuration, API discovery steps, and troubleshooting guidance.]

## Skill Version(s):

1.5.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
