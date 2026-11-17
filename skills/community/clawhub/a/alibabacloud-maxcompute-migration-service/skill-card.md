## Description: <br>
Guides agents through MaxCompute Migration Service planning, source and metadata lookup, target mapping, job and timer creation, monitoring, and managed migration mode with confirmation gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data engineers, and cloud administrators use this skill to plan and operate migrations from supported external data sources into Alibaba Cloud MaxCompute. It helps resolve MMS source identifiers, inspect metadata, configure target mappings, draft and run Aliyun CLI commands, monitor jobs and tasks, and verify migration results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First-run setup may ask users to run a remote Aliyun CLI installer and enable automatic plugin installation in a high-impact cloud administration context. <br>
Mitigation: Install only in a controlled admin environment; prefer package-manager or internally approved Aliyun CLI and plugin versions, and review or disable automatic plugin installation where appropriate. <br>
Risk: Migration operations can create, start, stop, retry, or schedule cloud data movement jobs with broad operational impact. <br>
Mitigation: Use least-privilege, preferably short-lived credentials scoped to the migration; require explicit user confirmation before create/start/stop/delete actions; and verify mappings, source IDs, and job names before execution. <br>
Risk: Incorrect source ID resolution, target mapping, or metadata assumptions could migrate the wrong scope or report misleading progress. <br>
Mitigation: Apply bounded source_id discovery, strict equality checks for LIKE-based name matches, current mapping inspection before updates, and table/partition status checks before job creation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-maxcompute-migration-service) <br>
- [MMS Overview](https://help.aliyun.com/zh/maxcompute/user-guide/migration-service-mms) <br>
- [MMS Preparation](https://help.aliyun.com/zh/maxcompute/user-guide/mms-preparation) <br>
- [Manage Data Sources](https://help.aliyun.com/zh/maxcompute/user-guide/manage-data-sources) <br>
- [Create and Execute Migration Jobs](https://help.aliyun.com/zh/maxcompute/user-guide/create-and-execute-a-migration-job) <br>
- [Migration Monitoring](https://help.aliyun.com/zh/maxcompute/user-guide/migration-observation) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [MMS Commands - Data Source and Metadata](references/commands-datasource-and-metadata.md) <br>
- [MMS Commands - Mapping and Planning](references/commands-mapping-and-planning.md) <br>
- [MMS Commands - Job, Timer, Task and Async](references/commands-job-timer-task.md) <br>
- [MMS Source ID Resolution Rules](references/mms-source-id-and-resolution.md) <br>
- [RAM Policies for MMS](references/ram-policies.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [OpenAPI Checklist](references/openapi-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Analysis] <br>
**Output Format:** [Markdown responses with Aliyun CLI command blocks, confirmation tables, status reports, and verification steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands should include the required MMS user-agent, use bounded lookup rules, avoid plaintext credential handling, and require explicit confirmation before create/start/stop/delete actions.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
