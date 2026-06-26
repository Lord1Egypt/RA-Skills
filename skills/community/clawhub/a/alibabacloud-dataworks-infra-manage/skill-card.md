## Description: <br>
Manages Alibaba Cloud DataWorks data sources, compute resources, serverless resource groups, connectivity tests, and resource group bindings through aliyun CLI commands for dataworks-public OpenAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to inspect and initialize DataWorks workspace infrastructure, create supported data sources and compute resources, manage serverless resource group bindings, and test connectivity while following documented confirmation and security gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide cloud infrastructure write operations and references permissions for billing, resource groups, and workspace members beyond some routine DataWorks tasks. <br>
Mitigation: Use a least-privilege RAM policy, exclude workspace member APIs unless explicitly needed, and grant BSS payment permissions only when creating billable resource groups. <br>
Risk: Commands may run against the wrong Alibaba Cloud account, region, workspace, VPC, VSwitch, or resource group if context is assumed. <br>
Mitigation: Confirm the active Aliyun profile, account, region, workspace, and all user-selectable networking or resource group parameters before every write. <br>
Risk: Database credentials, access keys, or tokens could be exposed through chat, command lines, logs, or committed files. <br>
Mitigation: Use configured Aliyun profiles and credential files, avoid pasting secrets into chat or shell history, and never print or echo AK/SK values. <br>


## Reference(s): <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>
- [DataWorks Infrastructure RAM Policies](references/ram-policies.md) <br>
- [DataWorks Infrastructure Related APIs](references/related-apis.md) <br>
- [DataWorks Data Sources Reference](references/data-sources/README.md) <br>
- [Compute Resource ConnectionProperties Reference](references/compute-resources/README.md) <br>
- [Cross-Account Data Source Configuration](references/cross-account-datasources.md) <br>
- [Alibaba Cloud CLI Documentation](https://help.aliyun.com/zh/cli/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands, JSON parameter examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Aliyun CLI commands, DataWorks OpenAPI parameter templates, RAM permission guidance, pre-execution confirmations, connectivity troubleshooting, and follow-up steps.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
