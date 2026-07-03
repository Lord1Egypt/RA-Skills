## Description: <br>
Automates Alibaba Cloud Yunxiao DevOps tasks, including pipeline execution, code repository and merge request management, work item and sprint tracking, test case creation, artifact management, and application release workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to translate natural-language Yunxiao requests into confirmed CLI, MCP, or mcporter actions for CI/CD, code management, project collaboration, testing, artifacts, and application delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and run external CLI, npm, MCP, and mcporter tooling. <br>
Mitigation: Prefer manual, verified installation from official sources and pre-install required packages instead of using curl-to-shell or live npx downloads in privileged environments. <br>
Risk: The skill uses powerful Yunxiao Personal Access Tokens for DevOps operations. <br>
Mitigation: Use short-lived, least-privilege tokens stored as secrets or environment variables, and avoid command-line token parameters. <br>
Risk: Create, update, delete, and deployment actions can change repositories, pipelines, work items, artifacts, tests, or releases. <br>
Mitigation: Review every proposed write action, confirm all user-controlled parameters, and verify results with read-back commands after execution. <br>
Risk: Exposed MCP SSE endpoints can expand credential and tool access risk. <br>
Mitigation: Keep SSE endpoints local-only unless protected with authentication, TLS, and network controls. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-devops) <br>
- [Tool Catalog](references/tool-catalog.md) <br>
- [Product Mapping](references/product-mapping.md) <br>
- [Product Reference Index](references/product-reference.md) <br>
- [Yunxiao Alibaba Cloud CLI Configuration Reference](references/aliyun-cli-setup.md) <br>
- [Alibaba Cloud CLI Installation Guide](references/aliyun-cli-install.md) <br>
- [MCP Server Setup](references/mcp-setup.md) <br>
- [Yunxiao Personal Access Token Authorization Scopes](references/token-scopes.md) <br>
- [Success Verification Methods](references/verification-method.md) <br>
- [Yunxiao Product Documentation](https://help.aliyun.com/product/150040.html) <br>
- [Yunxiao OpenAPI Documentation](https://help.aliyun.com/zh/yunxiao/developer-reference/) <br>
- [alibabacloud-devops-mcp-server Package](https://www.npmjs.com/package/alibabacloud-devops-mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration snippets, and CLI or MCP call descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce executable DevOps commands that require user-confirmed parameters, configured credentials, and read-back verification for changes.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
