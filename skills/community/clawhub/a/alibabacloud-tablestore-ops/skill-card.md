## Description: <br>
Alibaba Cloud Tablestore (OTS) Read-Only Operations Skill for querying Tablestore instances and data tables via Aliyun CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to inspect Alibaba Cloud Tablestore instances and table metadata through read-only Aliyun CLI commands while confirming regions, endpoints, instance names, and table names with the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Supporting docs include examples that can grant broader Alibaba Cloud permissions than read-only workflows require. <br>
Mitigation: Use a dedicated RAM user or role with AliyunOTSReadOnlyAccess only, avoid FullAccess and CreateInstance examples, and review commands before use. <br>
Risk: CLI setup and configuration can expose or misuse cloud credentials. <br>
Mitigation: Configure credentials only through aliyun configure, do not echo AccessKeys or share raw Aliyun config output, and install Aliyun CLI only from trusted Alibaba Cloud sources. <br>


## Reference(s): <br>
- [Aliyun CLI Installation Guide](references/cli-installation-guide.md) <br>
- [Tablestore Read-Only RAM Policies](references/ram-policies.md) <br>
- [Tablestore CLI Related APIs Reference](references/related-apis.md) <br>
- [Tablestore Read-Only Verification Methods](references/verification-method.md) <br>
- [Tablestore Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Aliyun CLI GitHub](https://github.com/aliyun/aliyun-cli) <br>
- [Alibaba Cloud Tablestore Instance Operations](https://help.aliyun.com/zh/tablestore/developer-reference/instance-operations) <br>
- [Alibaba Cloud Tablestore Data Table Operations](https://help.aliyun.com/zh/tablestore/developer-reference/widecolumn-modeled-data-table-operations-with-tablestore-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Tablestore workflows; commands require user-confirmed region, endpoint, instance, table, and credential setup.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
