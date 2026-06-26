## Description: <br>
Manage Alibaba Cloud beebot (Chatbot) via OpenAPI/SDK. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to inventory, configure, troubleshoot, and verify Alibaba Cloud Chatbot resources through OpenAPI metadata, SDK calls, and API-level diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help perform high-impact Alibaba Cloud Chatbot create, update, delete, or configuration operations using cloud credentials. <br>
Mitigation: Use a restricted RAM user or role, require a written plan before mutating operations, and verify results with describe or list APIs. <br>
Risk: Region, tenant, or account scope may be unclear before an API call. <br>
Mitigation: Confirm the exact region and tenant/account before calling Alibaba Cloud APIs, especially for create, update, delete, or configuration changes. <br>
Risk: Credentialed API calls may exceed the user-intended permission scope. <br>
Mitigation: Install only when Alibaba Cloud Chatbot management is intended and prefer least-privilege credentials for the target resources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cinience/alicloud-ai-chatbot) <br>
- [Sources](references/sources.md) <br>
- [Alibaba Cloud Chatbot OpenAPI product page](https://api.aliyun.com/product/Chatbot) <br>
- [Alibaba Cloud Chatbot API metadata](https://api.aliyun.com/meta/v1/products/Chatbot/versions/2022-04-08/api-docs.json) <br>
- [Alibaba Cloud Chatbot single API metadata template](https://api.aliyun.com/meta/v1/products/Chatbot/versions/2022-04-08/apis/{ApiName}/api.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, configuration notes, and generated API inventory files when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes optional command outputs, API summaries, and generated artifacts under output/alicloud-ai-chatbot/.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
