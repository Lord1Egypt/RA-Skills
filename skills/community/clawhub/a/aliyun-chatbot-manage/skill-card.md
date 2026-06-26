## Description: <br>
Use when managing Alibaba Cloud beebot (Chatbot) via OpenAPI/SDK, including the user asks to configure, query, or troubleshoot Alibaba Cloud chatbot resources, including bot inventory, configuration changes, status checks, and API-level diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to manage Alibaba Cloud beebot (Chatbot) resources through OpenAPI or SDK workflows, including inventory, configuration changes, status checks, and API-level diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide changes to Alibaba Cloud Chatbot resources. <br>
Mitigation: Use a least-privilege RAM user or role and require explicit approval before any mutating API call. <br>
Risk: Incorrect region or resource identifiers could target the wrong Alibaba Cloud resources. <br>
Mitigation: Confirm region, resource IDs, and intended action before calling APIs, and ask the user when the region is unclear. <br>
Risk: Saved outputs may contain API response details or operational context. <br>
Mitigation: Review files under output/aliyun-chatbot-manage/ before sharing or committing them. <br>


## Reference(s): <br>
- [Skill source references](references/sources.md) <br>
- [Alibaba Cloud Chatbot OpenAPI product page](https://api.aliyun.com/product/Chatbot) <br>
- [Alibaba Cloud Chatbot API metadata](https://api.aliyun.com/meta/v1/products/Chatbot/versions/2022-04-08/api-docs.json) <br>
- [Alibaba Cloud Chatbot single API definition template](https://api.aliyun.com/meta/v1/products/Chatbot/versions/2022-04-08/apis/{ApiName}/api.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and saved JSON or Markdown evidence files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated artifacts and API response summaries should be saved under output/aliyun-chatbot-manage/.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
