## Description: <br>
Feishu Messaging 0 helps agents send Feishu messages, look up group IDs and members, create documents, and retry failed message workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xq-8](https://clawhub.ai/user/xq-8) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and developers who use Feishu or Lark bots can use this skill to prepare API-based workflows for sending messages, uploading images or files, and finding group or member identifiers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages or uploads could be sent to the wrong recipient or with unintended content. <br>
Mitigation: Explicitly confirm the recipient, message text, and exact file path before sending messages or uploading content. <br>
Risk: Feishu/Lark app credentials and broad API scopes could expose workspace data if mishandled. <br>
Mitigation: Protect the app secret and use least-privilege app scopes for the intended bot workflow. <br>


## Reference(s): <br>
- [Feishu Open Platform API documentation](https://open.feishu.cn/document/server-docs/api-call-guide/server-api-list) <br>
- [ClawHub skill page](https://clawhub.ai/xq-8/feishu-messaging-0) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown with Python code blocks and API permission notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Feishu/Lark recipient, file path, and credential placeholders for user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
