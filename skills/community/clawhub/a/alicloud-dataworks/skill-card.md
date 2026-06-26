## Description: <br>
Operate Alibaba Cloud DataWorks through dynamic API discovery and official SDKs for data development, workflow operations, data integration, data quality, metadata lineage, and workspace management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samuelhsin](https://clawhub.ai/user/samuelhsin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to discover Alibaba Cloud DataWorks APIs and operate projects, workflows, metadata, data quality, and related resources through SDKs, OpenAPI metadata, or MCP integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to manage or mutate Alibaba Cloud DataWorks resources. <br>
Mitigation: Use scoped RAM or temporary credentials, review proposed changes before allowing mutations, and confirm destructive operations before execution. <br>
Risk: The metadata helper scripts include an insecure TLS fallback. <br>
Mitigation: Prefer verified HTTPS metadata fetching and review downloaded metadata before relying on it. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/samuelhsin/alicloud-dataworks) <br>
- [Sources](references/sources.md) <br>
- [MCP Server integration](references/mcp_server.md) <br>
- [DataWorks documentation](https://www.alibabacloud.com/help/dataworks) <br>
- [OpenAPI Explorer](https://api.aliyun.com/product/dataworks-public) <br>
- [DataWorks OpenAPI metadata](https://next.api.aliyun.com/meta/v1/products/dataworks-public/versions/2024-05-18/api-docs.json) <br>
- [DataWorks MCP Server npm package](https://www.npmjs.com/package/alibabacloud-dataworks-mcp-server) <br>
- [DataWorks MCP Server GitHub](https://github.com/aliyun/alibabacloud-dataworks-mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated output files under output/dataworks-open-api when helper scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
