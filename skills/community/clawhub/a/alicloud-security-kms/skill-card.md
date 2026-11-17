## Description:

Manage Alibaba Cloud Key Management Service (KMS) via OpenAPI/SDK for key lifecycle and resource operations, policy and configuration changes, status inspection, and troubleshooting KMS API workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud operators, and security engineers use this skill to guide Alibaba Cloud KMS administration, including metadata-first API discovery, key lifecycle operations, configuration changes, and verification with list or describe APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide powerful Alibaba Cloud KMS administration actions, including mutating Create, Update, Modify, and Set API calls.

Mitigation: Use narrowly scoped Alibaba Cloud credentials and review any mutating API call before execution.

Risk: Saved API discovery outputs or operation results may contain cloud resource details.

Mitigation: Keep generated outputs under output/alicloud-security-kms/ and review them before sharing.

## Reference(s):

- [Alibaba Cloud KMS OpenAPI product page](https://api.aliyun.com/product/Kms)
- [Alibaba Cloud KMS API metadata](https://api.aliyun.com/meta/v1/products/Kms/versions/2016-01-20/api-docs.json)
- [Alibaba Cloud KMS single API metadata template](https://api.aliyun.com/meta/v1/products/Kms/versions/2016-01-20/apis/{ApiName}/api.json)
- [ClawHub skill page](https://clawhub.ai/cinience/skills/alicloud-security-kms)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Markdown, API Calls]

**Output Format:** [Markdown with inline shell commands and generated JSON or Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated discovery artifacts and operation outputs should be kept under output/alicloud-security-kms/.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
