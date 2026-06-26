## Description: <br>
MaxCompute Quota Management Skill for managing MaxCompute/ODPS quota resources, including pay-as-you-go quota creation, query, and listing operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to list, query, and create Alibaba Cloud MaxCompute/ODPS pay-as-you-go quota resources through Aliyun CLI workflows. It is intended for accounts where the user can confirm region, billing, credential, and permission choices before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Aliyun CLI credentials to inspect and create MaxCompute quota resources, which may affect billable cloud resources. <br>
Mitigation: Use narrowly scoped RAM permissions, confirm all user-customizable parameters before execution, and review intended create operations before running them. <br>
Risk: Credential and permission guidance may be overbroad if copied into a production account without review. <br>
Mitigation: Avoid broad MaxComputeFullAccess-style policies unless intentionally needed, do not paste real AccessKeys into chat or command lines, and prefer scoped quota-resource permissions. <br>
Risk: The workflow may create local output and action-log files containing operational details. <br>
Mitigation: Review generated files after use and delete them when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-odps-quota-manage) <br>
- [Related APIs](references/related-apis.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [MaxCompute Product](https://api.aliyun.com/product/MaxCompute) <br>
- [CreateQuota API](https://api.aliyun.com/api/MaxCompute/2022-01-04/CreateQuota) <br>
- [ListQuotas API](https://api.aliyun.com/api/MaxCompute/2022-01-04/ListQuotas) <br>
- [Alibaba Cloud SDK credential management](https://help.aliyun.com/zh/sdk/developer-reference/v2-manage-access-credentials) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API Calls, Files, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local output and action-log files after running quota workflows.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
