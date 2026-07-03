## Description: <br>
Batch health inspection for Alibaba Cloud RDS PostgreSQL instances that runs Aliyun CLI checks and produces per-instance and summary HTML reports covering resource use, alerts, slow logs, long transactions, table bloat, QPS/TPS, and replication delay. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, database administrators, and cloud operations teams use this skill to inspect selected Alibaba Cloud RDS PostgreSQL instances or broader fleets and collect health reports for operational review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs Aliyun CLI commands, installs or updates Aliyun CLI plugins, and writes detailed inspection reports locally. <br>
Mitigation: Use a least-privilege read-only RAM identity or temporary credentials, review CLI/plugin changes before use, and run in a controlled workspace. <br>
Risk: Generated reports can contain sensitive operational data about RDS instances, alerts, slow queries, and resource utilization. <br>
Mitigation: Protect report directories as sensitive data and delete them when they are no longer needed. <br>
Risk: Opening generated HTML reports may contact a third-party CDN for chart assets. <br>
Mitigation: Open reports only in an environment where that network access is acceptable, or review the HTML before opening. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-rds-postgresql-inspection) <br>
- [RAM Permissions Reference](references/ram-policies.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Aliyun CLI Installation Guide](assets/cli-installation-guide.md) <br>
- [Alibaba Cloud RDS API](https://help.aliyun.com/zh/rds/developer-reference/) <br>
- [Alibaba Cloud CMS API](https://help.aliyun.com/zh/cms/cloudmonitor-1-0/developer-reference/) <br>
- [Aliyun CLI Documentation](https://help.aliyun.com/zh/cli/) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [HTML reports with concise Markdown/status text and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes one HTML report per inspected instance and writes summary.html when all-instance mode is used.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
