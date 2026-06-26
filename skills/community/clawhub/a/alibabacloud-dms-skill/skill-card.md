## Description: <br>
Search for target databases in Alibaba Cloud DMS and execute SQL queries or data modifications through the Aliyun CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to locate Alibaba Cloud DMS databases and run reviewed SQL queries or limited data modifications with their configured Alibaba Cloud identity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read or change databases using the user's configured Alibaba Cloud identity. <br>
Mitigation: Use a dedicated low-privilege RAM user or temporary credentials, prefer read-only permissions, and confirm the database ID and full SQL before execution. <br>
Risk: Write SQL can modify database data. <br>
Mitigation: Preview INSERT, UPDATE, and DELETE statements with --dry-run first; execute them only with --force after review. DDL operations are blocked by the script and should be handled through the DMS Console. <br>
Risk: AI-Mode and CLI plugin settings can affect later Aliyun CLI usage if left enabled. <br>
Mitigation: Disable AI-Mode after each session and review the CLI auto-plugin-install setting after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-dms-skill) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [RAM Policies for DMS Database Query](references/ram-policies.md) <br>
- [Related APIs for DMS Database Query](references/related-apis.md) <br>
- [Acceptance Criteria: DMS Database Query](references/acceptance-criteria.md) <br>
- [DMS OpenAPI Overview](https://api.aliyun.com/product/dms-enterprise) <br>
- [Alibaba Cloud DMS API Reference](https://help.aliyun.com/zh/dms/developer-reference/) <br>
- [DMS Permission Management](https://help.aliyun.com/zh/dms/user-guide/permission-management) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Text and JSON command output with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Aliyun CLI, jq, configured Alibaba Cloud credentials, a database keyword, a database ID, and a SQL statement.] <br>

## Skill Version(s): <br>
0.0.2 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
