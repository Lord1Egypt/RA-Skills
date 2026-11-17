## Description:

Helps agents manage Alibaba Cloud ID Verification (Cloudauth) workflows through OpenAPI metadata discovery, SDK/OpenAPI Explorer guidance, status checks, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud security engineers use this skill to discover Cloudauth APIs, plan or execute resource operations, validate configuration, and collect reproducible evidence for Alibaba Cloud identity-verification workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide mutating Alibaba Cloud API operations that change identity-verification resources or configuration.

Mitigation: Use least-privilege Alibaba Cloud credentials and review any mutating API call before execution.

Risk: Output artifacts may accidentally include secrets, full identity records, or unredacted customer data.

Mitigation: Redact secrets and sensitive identity data before saving artifacts under output/aliyun-cloudauth-verify/.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-cloudauth-verify)
- [Alibaba Cloud Cloudauth OpenAPI product page](https://api.aliyun.com/product/Cloudauth)
- [Cloudauth 2022-11-25 API metadata list](https://api.aliyun.com/meta/v1/products/Cloudauth/versions/2022-11-25/api-docs.json)
- [Cloudauth single API metadata template](https://api.aliyun.com/meta/v1/products/Cloudauth/versions/2022-11-25/apis/{ApiName}/api.json)
- [Skill sources reference](references/sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON or Markdown artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save API inventory and evidence artifacts under output/aliyun-cloudauth-verify/.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
