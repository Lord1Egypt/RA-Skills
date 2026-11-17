## Description:

Helps agents manage Alibaba Cloud beebot (Chatbot) resources through OpenAPI/SDK workflows for inventory, configuration, status checks, and diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to configure, query, and troubleshoot Alibaba Cloud Chatbot resources while confirming region, resource identifiers, and intended changes before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide live changes to Alibaba Cloud Chatbot resources.

Mitigation: Use least-privilege Alibaba Cloud credentials and confirm the exact region, resource ID, and intended change before any mutation.

Risk: Saved outputs could expose sensitive API response details or secrets if handled carelessly.

Mitigation: Keep secrets out of saved artifacts and store outputs only under output/aliyun-chatbot-manage/ for review.

## Reference(s):

- [Alibaba Cloud Chatbot OpenAPI product page](https://api.aliyun.com/product/Chatbot)
- [Alibaba Cloud Chatbot API metadata](https://api.aliyun.com/meta/v1/products/Chatbot/versions/2022-04-08/api-docs.json)
- [Alibaba Cloud Chatbot single API metadata](https://api.aliyun.com/meta/v1/products/Chatbot/versions/2022-04-08/apis/{ApiName}/api.json)
- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-chatbot-manage)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, code snippets, configuration notes, and optional saved files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save API inventories, command outputs, and response summaries under output/aliyun-chatbot-manage/.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
