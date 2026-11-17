## Description:

Manages Alibaba Cloud Content Moderation (Green) resources and policies through OpenAPI/SDK workflows, including listing, creating, updating, status checks, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud or security operators use this skill to manage Alibaba Cloud Content Moderation (Green) resources and policies, discover relevant OpenAPI operations, and prepare or review API calls. It supports credential-aware administration for inventory, configuration changes, status inspection, and workflow troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help prepare Alibaba Cloud API calls that create, update, modify, or set moderation resources and policies.

Mitigation: Use least-privilege Alibaba Cloud credentials and review any mutating operation before execution.

Risk: Saved API responses or command artifacts may contain operational details from the user's Alibaba Cloud environment.

Mitigation: Keep generated outputs in the documented output directory and avoid storing secrets in evidence files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-green-moderation)
- [Alibaba Cloud OpenAPI Green product page](https://api.aliyun.com/product/Green)
- [Alibaba Cloud Green API metadata list](https://api.aliyun.com/meta/v1/products/Green/versions/2022-09-26/api-docs.json)
- [Alibaba Cloud Green single API definition metadata](https://api.aliyun.com/meta/v1/products/Green/versions/2022-09-26/apis/{ApiName}/api.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Files]

**Output Format:** [Markdown with inline shell commands and saved JSON or Markdown artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated responses and API evidence should be stored under output/aliyun-green-moderation/.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
