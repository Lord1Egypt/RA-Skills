## Description: <br>
Batch export Alibaba Cloud WAF 3.0 CNAME-based domain configuration to Excel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud security engineers and operations teams use this skill to inspect Alibaba Cloud WAF 3.0 CNAME domain settings across Chinese Mainland and Non-Chinese Mainland instances and produce an audit-ready Excel export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires cloud credentials and read access to Alibaba Cloud WAF configuration. <br>
Mitigation: Use short-lived or least-privileged RAM credentials, avoid putting real access keys in shell commands or logs, and verify credentials only through the configured Aliyun CLI profile. <br>
Risk: The generated Excel workbook can contain sensitive infrastructure details such as domains, CNAMEs, backends, certificates, TLS settings, and resource groups. <br>
Mitigation: Choose and review the export location before execution, restrict access to the workbook, and handle it as sensitive infrastructure data. <br>
Risk: The workflow includes an additional DescribeDomainDetail probe when a discovered instance has no domains. <br>
Mitigation: Review the extra probe behavior before use and ensure the configured RAM policy permits only the documented read-only WAF actions. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/sdk-team/alibabacloud-waf-cname-config-export) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Related CLI Commands](references/related-commands.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [DescribeDomains API](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/developer-reference/api-waf-openapi-2021-10-01-describedomains) <br>
- [DescribeDomainDetail API](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/developer-reference/api-waf-openapi-2021-10-01-describedomaindetail) <br>
- [DescribeInstance API](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/developer-reference/api-waf-openapi-2021-10-01-describeinstance) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, files] <br>
**Output Format:** [Markdown guidance with bash commands and a generated Excel workbook] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a timestamped waf_cname_config_export_YYYYMMDD_HHMMSS.xlsx file with one sheet per queried region and an 18-column WAF domain configuration schema.] <br>

## Skill Version(s): <br>
0.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
