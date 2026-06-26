## Description: <br>
DataWorks Data Quality (Read-Only) helps agents query Alibaba Cloud DataWorks rule templates, data quality monitors, alert rules, scan run records, and scan logs through read-only aliyun CLI OpenAPI calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data engineers, and operations teams use this skill to inspect Alibaba Cloud DataWorks data quality configuration and diagnose failed or warning scan runs without changing workspace resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses local aliyun CLI configuration and cloud credentials to query DataWorks resources. <br>
Mitigation: Review the CLI setup commands before use, verify credentials only with `aliyun configure list`, and do not paste access keys or secret keys into chat. <br>
Risk: Returned scan logs, alert rules, and monitor details may expose operational details or recipient information. <br>
Mitigation: Limit use to authorized workspaces and share summarized results only with users who are allowed to view the underlying DataWorks data. <br>
Risk: Over-broad RAM permissions could allow more access than this read-only workflow requires. <br>
Mitigation: Use least-privilege read-only RAM permissions for the listed DataWorks Get/List APIs and keep write permissions out of the agent workflow. <br>
Risk: Requests to create, update, delete, or manually trigger DataWorks data quality resources are outside the skill's intended behavior. <br>
Mitigation: Block write or trigger requests and direct users to the DataWorks console for configuration changes. <br>


## Reference(s): <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>
- [DataWorks Data Quality RAM Policies](references/ram-policies.md) <br>
- [DataWorks Data Quality Related APIs](references/related-apis.md) <br>
- [Aliyun CLI Official Documentation](https://help.aliyun.com/zh/cli/) <br>
- [DataWorks RAM Permission Guide](https://help.aliyun.com/zh/dataworks/user-guide/dataworks-ram-permissions) <br>
- [ListDataQualityTemplates API](https://help.aliyun.com/zh/dataworks/developer-reference/api-dataworks-public-2024-05-18-listdataqualitytemplates) <br>
- [GetDataQualityTemplate API](https://help.aliyun.com/zh/dataworks/developer-reference/api-dataworks-public-2024-05-18-getdataqualitytemplate) <br>
- [ListDataQualityScans API](https://help.aliyun.com/zh/dataworks/developer-reference/api-dataworks-public-2024-05-18-listdataqualityscans) <br>
- [GetDataQualityScan API](https://help.aliyun.com/zh/dataworks/developer-reference/api-dataworks-public-2024-05-18-getdataqualityscan) <br>
- [ListDataQualityAlertRules API](https://help.aliyun.com/zh/dataworks/developer-reference/api-dataworks-public-2024-05-18-listdataqualityalertrules) <br>
- [GetDataQualityAlertRule API](https://help.aliyun.com/zh/dataworks/developer-reference/api-dataworks-public-2024-05-18-getdataqualityalertrule) <br>
- [ListDataQualityScanRuns API](https://help.aliyun.com/zh/dataworks/developer-reference/api-dataworks-public-2024-05-18-listdataqualityscanruns) <br>
- [GetDataQualityScanRun API](https://help.aliyun.com/zh/dataworks/developer-reference/api-dataworks-public-2024-05-18-getdataqualityscanrun) <br>
- [GetDataQualityScanRunLog API](https://help.aliyun.com/zh/dataworks/developer-reference/api-dataworks-public-2024-05-18-getdataqualityscanrunlog) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only DataWorks query guidance; list results are summarized rather than dumped as raw JSON.] <br>

## Skill Version(s): <br>
0.0.1-beta.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
