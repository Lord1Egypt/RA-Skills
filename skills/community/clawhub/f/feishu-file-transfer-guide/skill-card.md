## Description: <br>
Guides agents through uploading local files to Feishu and sending them as file messages using Feishu Open Platform APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swingmonkey](https://clawhub.ai/user/swingmonkey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill as a practical guide for sending local files to Feishu users from OpenClaw Agent workflows. It explains how to obtain a tenant access token, upload a file for a file_key, and send a Feishu file message. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The sample Python code disables HTTPS certificate verification while handling app secrets, tokens, and uploaded files. <br>
Mitigation: Restore certificate verification before running the examples and review the code before use. <br>
Risk: Feishu credentials, access tokens, local files, and recipient IDs may be exposed or misused if handled carelessly. <br>
Mitigation: Use least-privilege Feishu credentials, store secrets outside source code, avoid logging tokens, and confirm the selected file and recipient before uploading. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/swingmonkey/feishu-file-transfer-guide) <br>
- [Feishu Open Platform - Upload file](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/file/create) <br>
- [Feishu Open Platform - Send message](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guide with JSON, PowerShell, and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-supplied Feishu app credentials, recipient ID, and local file path; sample code should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
