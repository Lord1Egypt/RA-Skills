## Description: <br>
Alibaba Cloud MaxCompute Migration Service (MMS) helps agents guide migrations from Hive, BigQuery, Databricks, Snowflake, Redshift, and MaxCompute into MaxCompute. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data engineers, and cloud operators use this skill to plan, run, monitor, and troubleshoot MaxCompute MMS migrations while confirming parameters and protecting credentials. <br>

### Deployment Geography for Use: <br>
Global, subject to MaxCompute MMS availability in documented Alibaba Cloud regions. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect real MaxCompute migration jobs and data access when used with live Alibaba Cloud credentials. <br>
Mitigation: Use a dedicated least-privilege RAM profile, confirm every region, source, job, and task identifier before action, and avoid broad administrative grants unless temporarily approved. <br>
Risk: MMS data source details and cloud profiles may expose sensitive credentials. <br>
Mitigation: Configure credentials outside the agent session, never paste or print secrets, and sanitize API responses before displaying them or writing files. <br>
Risk: Create, stop, retry, resume, or delete operations can alter migration state. <br>
Mitigation: Confirm user intent, resolve names to IDs, check current resource state, and present ambiguous matches for user selection before executing state-changing commands. <br>


## Reference(s): <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [RAM Policies for MaxCompute Migration Service](references/ram-policies.md) <br>
- [MMS OpenAPI and CLI Commands](references/related-commands.md) <br>
- [Verification Method for MaxCompute Migration Service](references/verification-method.md) <br>
- [Alibaba Cloud MaxCompute Migration Service documentation](https://help.aliyun.com/zh/maxcompute/user-guide/migration-service-mms) <br>
- [MMS preparation documentation](https://help.aliyun.com/zh/maxcompute/user-guide/mms-preparation) <br>
- [Manage MMS data sources](https://help.aliyun.com/zh/maxcompute/user-guide/manage-data-sources) <br>
- [Create and execute a migration job](https://help.aliyun.com/zh/maxcompute/user-guide/create-and-execute-a-migration-job) <br>
- [Migration observation documentation](https://help.aliyun.com/zh/maxcompute/user-guide/migration-observation) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash, JSON, and SQL examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes CLI commands that require user-confirmed parameters and credential sanitization before display or file writes.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
