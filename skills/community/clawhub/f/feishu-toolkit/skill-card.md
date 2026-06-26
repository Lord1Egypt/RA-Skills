## Description: <br>
Complete Feishu (Lark) integration toolkit for AI agents to read and write documents, fetch chat history, send files and screenshots, manage permissions, and create scheduled reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ye4wzp](https://clawhub.ai/user/ye4wzp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers use this skill to let an agent work with Feishu or Lark documents, chats, file uploads, screenshots, permissions, and scheduled reminders through Feishu APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad Feishu or Lark workspace access, including document writes, chat-history reads, file or screenshot sends, permission changes, and scheduled reminders. <br>
Mitigation: Use a dedicated low-privilege Feishu app, grant only the scopes required for the intended workflow, and require explicit user approval before sensitive reads, writes, sends, permission changes, or reminder creation. <br>
Risk: Tenant-wide or admin-capable Feishu credentials could expand the impact of mistaken or unintended agent actions. <br>
Mitigation: Avoid tenant-wide or admin-capable credentials unless the deployment owner has reviewed and accepted the workspace impact. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ye4wzp/feishu-toolkit) <br>
- [Feishu Open Platform](https://open.feishu.cn/app) <br>
- [Feishu API Documentation](https://open.feishu.cn/document) <br>
- [Feishu Open API Base URL](https://open.feishu.cn/open-apis) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code, configuration] <br>
**Output Format:** [Markdown with API examples, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FEISHU_APP_ID and FEISHU_APP_SECRET for Feishu tenant access token authentication.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
