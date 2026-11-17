## Description:

Manage Alibaba Cloud Contact Center AI (ContactCenterAI) via OpenAPI/SDK. Use whenever the task involves Contact Center AI resource lifecycle operations, configuration changes, status queries, or troubleshooting failed ContactCenterAI API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations teams use this skill to manage Alibaba Cloud Contact Center AI resources, discover API schemas, make lifecycle or configuration changes, and troubleshoot ContactCenterAI API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide Create, Update, Modify, or Set operations against ContactCenterAI resources.

Mitigation: Confirm region, resource identifiers, and intended changes before execution, and review proposed mutating API calls before running them.

Risk: Cloud credentials may grant broader Alibaba Cloud access than the task requires.

Mitigation: Use least-privilege Alibaba Cloud credentials and prefer environment variables or the documented shared credentials file.

Risk: Saved API responses and generated artifacts may contain operational details.

Mitigation: Store generated artifacts only under output/alicloud-ai-contactcenter-ai/ and handle them according to the workspace data policy.

## Reference(s):

- [OpenAPI product page](https://api.aliyun.com/product/ContactCenterAI)
- [ContactCenterAI API list metadata](https://api.aliyun.com/meta/v1/products/ContactCenterAI/versions/2024-06-03/api-docs.json)
- [ContactCenterAI single API definition metadata](https://api.aliyun.com/meta/v1/products/ContactCenterAI/versions/2024-06-03/apis/{ApiName}/api.json)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, files]

**Output Format:** [Markdown with inline shell commands, file paths, and generated JSON or Markdown artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated API inventory artifacts should be written under output/alicloud-ai-contactcenter-ai/.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
