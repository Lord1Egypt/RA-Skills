## Description:

Manage Alibaba Cloud Cloud Firewall (Cloudfw) via OpenAPI/SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to manage Alibaba Cloud Cloud Firewall resources, firewall policy changes, status checks, and troubleshooting workflows through Alibaba Cloud OpenAPI metadata, SDKs, or OpenAPI Explorer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Firewall Create, Update, Modify, or Set operations can change network security posture.

Mitigation: Review planned mutating operations before execution and use describe or list APIs to verify the resulting state.

Risk: Alibaba Cloud credentials or sensitive API responses could be exposed through local artifacts.

Mitigation: Use least-privilege Alibaba Cloud credentials and avoid saving AccessKeys or sensitive API response contents in the output directory.

## Reference(s):

- [Alibaba Cloud Cloud Firewall OpenAPI product page](https://api.aliyun.com/product/Cloudfw)
- [Cloud Firewall API list metadata](https://api.aliyun.com/meta/v1/products/Cloudfw/versions/2017-12-07/api-docs.json)
- [Cloud Firewall single API definition metadata](https://api.aliyun.com/meta/v1/products/Cloudfw/versions/2017-12-07/apis/{ApiName}/api.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated JSON or Markdown evidence files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write API inventory artifacts and response summaries under output/alicloud-security-cloudfw/.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
