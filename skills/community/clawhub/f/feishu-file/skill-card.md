## Description: <br>
Send local files to Feishu chats, supporting upload and delivery of any file type as a Feishu file message. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[franklu0819-lang](https://clawhub.ai/user/franklu0819-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send a selected local file to Feishu users or groups through a configured Feishu bot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A selected local file can be uploaded to an unintended Feishu user or group. <br>
Mitigation: Verify the exact file path, receiver ID, receiver type, and bot permissions before each run. <br>
Risk: Sensitive files can leave the local environment through Feishu upload. <br>
Mitigation: Avoid sending secrets or private documents unless the destination and Feishu workspace are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/franklu0819-lang/feishu-file) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu file upload API](https://open.feishu.cn/open-apis/im/v1/files) <br>
- [Feishu message send API](https://open.feishu.cn/open-apis/im/v1/messages) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Text] <br>
**Output Format:** [Shell script execution with terminal status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, Feishu app credentials, a local file path, and a receiver ID or FEISHU_RECEIVER.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
