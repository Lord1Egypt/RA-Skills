## Description:

Manage Alibaba Cloud ID Verification (Cloudauth) via OpenAPI/SDK for identity-verification resource operations, config updates, status checks, and troubleshooting Cloudauth API workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to manage Alibaba Cloud ID Verification (Cloudauth) resources, configuration changes, status checks, and troubleshooting through OpenAPI/SDK workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials or identity-verification records could be exposed through prompts, command output, or saved artifacts.

Mitigation: Use least-privilege Alibaba Cloud credentials, avoid writing raw identity records or secrets to files, and keep necessary outputs under the documented output directory.

Risk: Create, Update, Modify, or Set API actions can change Cloudauth resources or configuration.

Mitigation: Confirm region, resource identifiers, parameters, and intended action before running mutating operations; prefer list and describe calls to verify current state first.

## Reference(s):

- [Cloudauth OpenAPI product page](https://api.aliyun.com/product/Cloudauth)
- [Cloudauth 2022-11-25 API metadata](https://api.aliyun.com/meta/v1/products/Cloudauth/versions/2022-11-25/api-docs.json)
- [Cloudauth single API metadata endpoint](https://api.aliyun.com/meta/v1/products/Cloudauth/versions/2022-11-25/apis/{ApiName}/api.json)
- [Skill source references](references/sources.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown with inline bash and Python code blocks, plus optional JSON and Markdown artifact files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save API inventory artifacts under output/alicloud-security-id-verification-cloudauth/.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
