## Description: <br>
Performs batch inspection on Alibaba Cloud MSE Nacos instances by checking configuration count usage, connection count usage, QPS usage, and TPS usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud operators, and SREs use this skill to inspect Alibaba Cloud MSE Nacos usage, identify capacity threshold breaches, and produce reviewable recommendations for selected instances or regions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs Aliyun CLI read-only inspection commands against an Alibaba Cloud account. <br>
Mitigation: Install only when this inspection access is intended, confirm instance and region parameters before execution, and use a least-privilege RAM profile. <br>
Risk: Alibaba Cloud access keys or other credentials could be exposed in chat, command history, or shared logs. <br>
Mitigation: Prefer temporary credentials or role-based access, check credential status without printing secrets, and do not paste real access keys into chat or reports. <br>
Risk: Generated inspection reports may include operational usage details that should not be broadly shared. <br>
Mitigation: Review the generated Markdown report before sharing it and remove sensitive environment, instance, or capacity details when needed. <br>
Risk: Metric data can be incomplete because of missing permissions, unavailable Prometheus endpoints, empty query results, or timeouts. <br>
Mitigation: Mark unavailable metrics as no data or N/A, include failure reasons in the report, and verify results with the bundled verification method before acting on recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-mse-nacos-inspection) <br>
- [Aliyun CLI documentation](https://help.aliyun.com/document_detail/139508.html) <br>
- [MSE quotas and limits](https://help.aliyun.com/zh/mse/product-overview/mse-quotas-and-limits) <br>
- [Developer and Professional edition specifications](https://help.aliyun.com/zh/mse/product-overview/estimate-developer-edition-instances-and-professional-edition-instances) <br>
- [Enterprise edition capacity description](https://help.aliyun.com/zh/mse/product-overview/nacos-platinum-edition-capacity-description) <br>
- [PromQL Query Reference](artifact/references/promql-queries.md) <br>
- [RAM Policies](artifact/references/ram-policies.md) <br>
- [Related CLI Commands](artifact/references/related-commands.md) <br>
- [Verification Method](artifact/references/verification-method.md) <br>
- [Aliyun CLI Installation and Configuration Guide](artifact/references/cli-installation-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown inspection summary and generated .md report with tables, alert details, command snippets, and recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses read-only Aliyun CLI and Prometheus HTTP queries; requires Alibaba Cloud credentials and least-privilege RAM permissions.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
