## Description:

Manage Alibaba Cloud beebot (Chatbot) via OpenAPI/SDK. Use whenever the user asks to configure, query, or troubleshoot Alibaba Cloud chatbot resources, including bot inventory, configuration changes, status checks, and API-level diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage Alibaba Cloud beebot (Chatbot) resources through OpenAPI/SDK workflows, including inventory, configuration changes, status checks, troubleshooting, and API metadata discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to mutate Alibaba Cloud Chatbot resources in user accounts.

Mitigation: Use least-privilege Alibaba Cloud credentials and explicitly confirm region, resource identifiers, and desired action before mutating operations.

Risk: The metadata helper accepts product, version, and output-directory arguments, so unsafe values could write artifacts to unintended locations until path validation is added.

Mitigation: Use trusted product/version values and keep output paths under output/alicloud-ai-chatbot/.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinience/skills/alicloud-ai-chatbot)
- [Sources](references/sources.md)
- [Alibaba Cloud OpenAPI Chatbot product page](https://api.aliyun.com/product/Chatbot)
- [Chatbot 2022-04-08 API metadata list](https://api.aliyun.com/meta/v1/products/Chatbot/versions/2022-04-08/api-docs.json)
- [Chatbot single API metadata template](https://api.aliyun.com/meta/v1/products/Chatbot/versions/2022-04-08/apis/{ApiName}/api.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands and JSON/Markdown artifact files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create API inventory files under output/alicloud-ai-chatbot/ and may call Alibaba Cloud OpenAPI metadata endpoints.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
