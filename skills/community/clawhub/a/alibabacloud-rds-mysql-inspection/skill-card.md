## Description: <br>
Batch health inspection for Alibaba Cloud RDS MySQL instances, producing per-instance and summary HTML reports across metrics, alerts, slow logs, space use, kernel version, and expiration checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, database administrators, and cloud operators use this skill to inspect Alibaba Cloud RDS MySQL instances, compare health across one or many instances, and receive optimization guidance from generated reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML reports may contain infrastructure metadata and SQL details. <br>
Mitigation: Store reports in an approved location, restrict access, and delete them when no longer needed. <br>
Risk: All-instance scans can inspect broad Alibaba Cloud RDS inventory using the configured Aliyun CLI profile. <br>
Mitigation: Use least-privilege RAM permissions scoped to the needed regions or instances, and confirm any all-instance scan before execution. <br>


## Reference(s): <br>
- [RAM permissions reference](references/ram-policies.md) <br>
- [Alibaba Cloud RDS API documentation](https://help.aliyun.com/zh/rds/developer-reference/) <br>
- [Alibaba Cloud CMS API documentation](https://help.aliyun.com/zh/cms/cloudmonitor-1-0/developer-reference/) <br>
- [Alibaba Cloud DAS API documentation](https://help.aliyun.com/zh/das/developer-reference/) <br>
- [Alibaba Cloud CLI documentation](https://help.aliyun.com/zh/cli/) <br>


## Skill Output: <br>
**Output Type(s):** [text, HTML reports, shell commands, configuration, guidance] <br>
**Output Format:** [HTML files plus concise text guidance and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a summary report and one report per inspected instance; the inspection window is configurable from 1 to 30 days.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
