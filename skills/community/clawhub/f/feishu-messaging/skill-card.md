## Description: <br>
Guides agents through Feishu Open Platform workflows for finding chats or members and sending messages or uploads through a Feishu bot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jypjypjypjyp](https://clawhub.ai/user/jypjypjypjyp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to prepare Feishu API workflows for finding chats or members, sending bot messages, and uploading message attachments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages or uploaded files may be sent to unintended Feishu recipients or expose sensitive content. <br>
Mitigation: Confirm recipient IDs, message content, and file paths before sending or uploading; use least-privilege Feishu scopes and keep app secrets out of logs and shared chats. <br>


## Reference(s): <br>
- [Feishu Open Platform API Documentation](https://open.feishu.cn/document/server-docs/api-call-guide/server-api-list) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, API calls, configuration] <br>
**Output Format:** [Markdown with Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials, bot permissions, recipient identifiers, and local file paths for uploads.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
