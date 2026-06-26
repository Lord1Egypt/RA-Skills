## Description: <br>
Looks up Feishu Open API documentation for endpoint discovery, parameters, responses, scripts, and API error troubleshooting using web search and page fetch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deadblue22](https://clawhub.ai/user/deadblue22) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to find Feishu Open Platform API endpoints, understand request and response shapes, identify required permissions, and draft or troubleshoot Feishu API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to read local Feishu app credentials and use them for tenant API actions. <br>
Mitigation: Provide narrowly scoped credentials explicitly, avoid exposing unrelated local configuration secrets, and review credential-handling code before execution. <br>
Risk: Generated Feishu API calls may perform real create, update, delete, permission, message, file, document, or record operations. <br>
Mitigation: Review each generated API call and its required permissions before execution, especially operations that change data or access rights. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/deadblue22/feishu-api-lookup) <br>
- [Feishu Open Platform API Documentation](https://open.feishu.cn/document/server-docs/im-v1/message/create) <br>
- [Feishu Apifox API Mirror](https://feishu.apifox.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with API endpoint summaries, request details, response notes, and code snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Feishu API paths, headers, request and response JSON, permission requirements, pagination notes, and error-code guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
