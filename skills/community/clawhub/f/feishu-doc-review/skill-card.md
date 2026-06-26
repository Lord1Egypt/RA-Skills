## Description: <br>
飞书云文档修订工具，帮助代理对飞书文档中的文本添加高亮、下划线和文档级批注。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yipng05-max](https://clawhub.ai/user/yipng05-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and document reviewers use this skill to mark Feishu documents during review workflows by highlighting blocks, underlining block text, or adding document-level comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent authenticated changes to Feishu documents, including highlights, underlines, and comments. <br>
Mitigation: Require explicit user confirmation before each document write or comment post and restrict use to controlled Feishu tenants. <br>
Risk: The security evidence reports that the skill embeds or permits a reusable app secret. <br>
Mitigation: Remove any hardcoded or fallback app secret, rotate any exposed credential, and require secrets to come only from approved environment configuration before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yipng05-max/feishu-doc-review) <br>
- [Feishu comment API endpoint](https://open.feishu.cn/open-apis/drive/v1/files/{doc_token}/comments?file_type=docx) <br>
- [Feishu tenant access token endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and API action parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent Feishu document changes when executed with valid tenant credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
