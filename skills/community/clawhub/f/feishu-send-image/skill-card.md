## Description: <br>
Sends user-selected images or files to Feishu users or group chats using local Feishu app credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jlif](https://clawhub.ai/user/Jlif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a workflow needs to send a specific local image or file to a Feishu user or group chat after the user provides the file path and recipient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload and send a local file or image to a Feishu user or group chat. <br>
Mitigation: Confirm the exact file path, recipient ID, recipient type, and intended content before execution. <br>
Risk: The skill reads local Feishu app credentials from ~/.openclaw/openclaw.json. <br>
Mitigation: Use Feishu app credentials scoped only to the upload and message permissions needed for this workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Jlif/feishu-send-image) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu image upload API](https://open.feishu.cn/open-apis/im/v1/images) <br>
- [Feishu file upload API](https://open.feishu.cn/open-apis/im/v1/files) <br>
- [Feishu message send API](https://open.feishu.cn/open-apis/im/v1/messages) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and command output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local file path, Feishu recipient ID, recipient type, and Feishu app credentials in ~/.openclaw/openclaw.json.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
