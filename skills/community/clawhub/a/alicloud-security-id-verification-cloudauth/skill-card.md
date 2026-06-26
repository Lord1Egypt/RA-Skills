## Description: <br>
Manage Alibaba Cloud ID Verification (Cloudauth) via OpenAPI/SDK for identity-verification resource operations, configuration updates, status checks, and Cloudauth API troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud operators, and security engineers use this skill to discover and run Alibaba Cloud Cloudauth OpenAPI workflows for identity-verification resources. It supports inventory, configuration, status checks, troubleshooting, and evidence capture for Cloudauth API operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Alibaba Cloud credentials may authorize sensitive Cloudauth operations. <br>
Mitigation: Use a least-privilege RAM user or temporary STS credentials and confirm every mutating operation before execution. <br>
Risk: Saved API responses or evidence files may contain access keys, secrets, applicant PII, or unnecessary resource identifiers. <br>
Mitigation: Store only necessary summaries under the skill output directory and redact secrets, PII, and unnecessary identifiers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cinience/alicloud-security-id-verification-cloudauth) <br>
- [Sources](references/sources.md) <br>
- [Alibaba Cloud OpenAPI Cloudauth product page](https://api.aliyun.com/product/Cloudauth) <br>
- [Cloudauth OpenAPI metadata API list](https://api.aliyun.com/meta/v1/products/Cloudauth/versions/2022-11-25/api-docs.json) <br>
- [Cloudauth single API definition template](https://api.aliyun.com/meta/v1/products/Cloudauth/versions/2022-11-25/apis/{ApiName}/api.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, API Calls, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python code references, JSON API metadata, and Markdown evidence files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated artifacts should be written under output/alicloud-security-id-verification-cloudauth/.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
