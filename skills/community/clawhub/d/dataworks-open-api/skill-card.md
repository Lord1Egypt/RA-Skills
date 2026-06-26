## Description: <br>
Operate Alibaba Cloud DataWorks through dynamic API discovery and official SDKs for Node.js, Python, and Java, covering data development, workflow operations, data integration, data quality, metadata lineage, and workspace management without a hardcoded API list. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samuelhsin](https://clawhub.ai/user/samuelhsin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to discover Alibaba Cloud DataWorks APIs, prepare SDK or MCP-based calls, manage workspaces and workflows, and troubleshoot DataWorks operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through DataWorks create, deploy, stop, suspend, and delete operations when valid Alibaba Cloud credentials are available. <br>
Mitigation: Use least-privilege RAM permissions, prefer short-lived or brokered credentials, and require review before approving state-changing or destructive operations. <br>
Risk: Credential endpoints, static access keys, and MCP configuration files can expose Alibaba Cloud access if shared or stored insecurely. <br>
Mitigation: Keep MCP configuration files and credential endpoints private, avoid embedding static secrets in prompts or files, and rotate credentials when exposure is suspected. <br>
Risk: Discovery scripts include an SSL fallback path that can reduce transport integrity in untrusted environments. <br>
Mitigation: Run discovery scripts only in trusted environments and prefer normal TLS validation when fetching official API documentation or metadata. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samuelhsin/dataworks-open-api) <br>
- [Skill homepage](https://github.com/aliyun/alibabacloud-bigdata-skills/tree/main/skills/dataworks/open-api) <br>
- [Cookbook](references/cookbook.md) <br>
- [Sources](references/sources.md) <br>
- [MCP Server Integration](references/mcp_server.md) <br>
- [DataWorks documentation](https://www.alibabacloud.com/help/dataworks) <br>
- [OpenAPI Explorer](https://api.aliyun.com/product/dataworks-public) <br>
- [DataWorks MCP Server npm package](https://www.npmjs.com/package/alibabacloud-dataworks-mcp-server) <br>
- [DataWorks MCP Server GitHub repository](https://github.com/aliyun/alibabacloud-dataworks-mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline code blocks, shell commands, SDK examples, API parameters, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands or API request guidance that require user-supplied Alibaba Cloud region, project identifiers, and credentials.] <br>

## Skill Version(s): <br>
1.5.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
