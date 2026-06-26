## Description: <br>
Manage Alibaba Cloud DataWorks via OpenAPI/MCP Server for data development, workflow operations, data quality, metadata lineage, workspace management, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samuelhsin](https://clawhub.ai/user/samuelhsin) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers, data engineers, and operations teams use this skill to discover and invoke Alibaba Cloud DataWorks APIs for data development, operations, data quality, metadata, lineage, and workspace tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Alibaba Cloud credentials to make broad DataWorks changes. <br>
Mitigation: Use a dedicated least-privilege RAM user or temporary credentials scoped to the specific DataWorks project and required actions. <br>
Risk: Shared MCP configuration files can expose production access keys. <br>
Mitigation: Avoid storing production access keys in shared MCP config files and prefer controlled environment-specific credential handling. <br>
Risk: Dynamic MCP tools may expose more DataWorks actions than a task requires. <br>
Mitigation: Use TOOL_CATEGORIES or TOOL_NAMES to narrow the exposed tool set before using the skill. <br>
Risk: Create, update, delete, suspend, member, or role-change operations can affect live resources. <br>
Mitigation: Require explicit confirmation after summarizing affected resources before performing these operations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/samuelhsin/alicloud-dataworks-skill) <br>
- [MCP Server Integration](references/mcp_server.md) <br>
- [Sources](references/sources.md) <br>
- [OpenAPI product page](https://api.aliyun.com/product/dataworks-public) <br>
- [DataWorks API metadata](https://next.api.aliyun.com/meta/v1/products/dataworks-public/versions/2024-05-18/api-docs.json) <br>
- [MCP Server tools discovery](https://dataworks.data.aliyun.com/pop-mcp-tools) <br>
- [MCP Server metadata](https://dataworks.data.aliyun.com/mcp) <br>
- [MCP Server tools overview](https://dataworks.data.aliyun.com/dw-pop-mcptools) <br>
- [MCP Server GitHub](https://github.com/aliyun/alibabacloud-dataworks-mcp-server) <br>
- [MCP Server npm package](https://www.npmjs.com/package/alibabacloud-dataworks-mcp-server) <br>
- [DataWorks documentation](https://www.alibabacloud.com/help/dataworks) <br>
- [DataWorks MCP usage guide](https://www.alibabacloud.com/help/dataworks/user-guide/dataworks-mcp-server-function-usage) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Markdown] <br>
**Output Format:** [Markdown with inline shell, JSON configuration, and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write API inventory artifacts under output/alicloud-dataworks/ when the helper script is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
