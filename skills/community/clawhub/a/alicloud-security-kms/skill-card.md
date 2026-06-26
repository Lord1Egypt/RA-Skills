## Description: <br>
Manage Alibaba Cloud Key Management Service (KMS) via OpenAPI/SDK. Use whenever the user needs key lifecycle/resource operations, policy/configuration changes, status inspection, or troubleshooting KMS API workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to inspect, configure, and troubleshoot Alibaba Cloud KMS resources through OpenAPI metadata, SDK calls, and command-oriented workflows. It supports key lifecycle operations, policy and configuration changes, and status verification after the account, region, and resource identifiers are confirmed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: KMS create, update, disable, rotate, policy, or deletion actions can affect encryption keys and dependent Alibaba Cloud resources. <br>
Mitigation: Confirm the Alibaba Cloud account, region, key identifier, requested action, and expected impact before approving mutating operations; prefer read-only inspection first. <br>
Risk: Credential misuse or over-permissioned AccessKeys could expose sensitive KMS operations. <br>
Mitigation: Use least-privilege Alibaba Cloud credentials from environment variables or the shared credentials file, and avoid exposing credential values in prompts, logs, or saved artifacts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cinience/alicloud-security-kms) <br>
- [Alibaba Cloud KMS OpenAPI Product Page](https://api.aliyun.com/product/Kms) <br>
- [Alibaba Cloud KMS API Metadata List](https://api.aliyun.com/meta/v1/products/Kms/versions/2016-01-20/api-docs.json) <br>
- [Alibaba Cloud KMS API Definition Template](https://api.aliyun.com/meta/v1/products/Kms/versions/2016-01-20/apis/{ApiName}/api.json) <br>
- [Skill Sources](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python snippets, and optional JSON or Markdown API inventory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When saving responses or generated artifacts, the skill directs the agent to write them under output/alicloud-security-kms/.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
