## Description:

Manage Alibaba Cloud Content Moderation (Green) via OpenAPI/SDK for resource and policy operations, status inspection, and moderation workflow troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage Alibaba Cloud Content Moderation resources and policies, inspect moderation status, and troubleshoot content review workflows through OpenAPI or SDK flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud moderation operations may create or modify Alibaba Cloud resources or policies when credentials are configured.

Mitigation: Use least-privilege Alibaba Cloud credentials and review create, update, modify, and set operations before execution.

Risk: Generated API responses or saved artifacts may contain account-specific details.

Mitigation: Keep generated response summaries in output/alicloud-security-content-moderation-green/ and review them before sharing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cinience/skills/alicloud-security-content-moderation-green)
- [Alibaba Cloud OpenAPI Product Page for Green](https://api.aliyun.com/product/Green)
- [Green 2022-09-26 API Metadata List](https://api.aliyun.com/meta/v1/products/Green/versions/2022-09-26/api-docs.json)
- [Green 2022-09-26 Single API Metadata Template](https://api.aliyun.com/meta/v1/products/Green/versions/2022-09-26/apis/{ApiName}/api.json)
- [Bundled Sources Reference](artifact/references/sources.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, files]

**Output Format:** [Markdown guidance with inline shell commands, API parameters, and generated output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated API inventory and response summaries should be saved under output/alicloud-security-content-moderation-green/.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
