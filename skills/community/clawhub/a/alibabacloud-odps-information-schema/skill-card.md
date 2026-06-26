## Description: <br>
Query MaxCompute (ODPS) Information Schema metadata views for governance, auditing, cost and usage analysis across tenant-level or project-level views. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, platform engineers, and data governance teams use this skill to answer natural-language questions about MaxCompute Information Schema metadata, including table storage, query history, permissions, quota usage, failed tasks, and governance diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide broad SQL execution paths that exceed its stated read-only Information Schema purpose. <br>
Mitigation: Restrict use to explicit SELECT queries against MaxCompute Information Schema views and review generated SQL before execution. <br>
Risk: Returned metadata can expose sensitive tenant details such as privileges, identities, IPs, task history, and project settings. <br>
Mitigation: Install only for authorized users, use least-privilege read-only credentials, and handle query outputs as sensitive operational data. <br>
Risk: The custom SQL path may be inappropriate where only fixed metadata templates are intended. <br>
Mitigation: Avoid the custom SQL path unless broader SELECT execution is explicitly approved for the deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sdk-team/alibabacloud-odps-information-schema) <br>
- [MaxCompute Tenant-level Information Schema](https://help.aliyun.com/zh/maxcompute/user-guide/tenant-level-information-schema) <br>
- [Information Schema Views Reference](references/views-reference.md) <br>
- [Verified Queries](references/verified-queries.md) <br>
- [MCP Tools Reference](references/mcp-tools-reference.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Troubleshooting](references/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with SQL examples, MCP tool guidance, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce MaxCompute Information Schema SQL and odpscmd fallback commands; outputs can include sensitive metadata query results when executed.] <br>

## Skill Version(s): <br>
0.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
