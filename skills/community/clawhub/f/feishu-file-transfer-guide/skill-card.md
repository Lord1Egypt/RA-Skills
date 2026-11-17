## Description:

Guides agents through uploading local files to Feishu and sending them as file messages by obtaining a tenant access token, uploading the file, and sending the resulting file_key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swingmonkey](https://clawhub.ai/user/swingmonkey)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw Agent users and developers use this guide to send local files to Feishu recipients when the default message tool would otherwise send only a path. It explains the token, upload, and message-send API flow with PowerShell and Python examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example code disables HTTPS certificate and hostname verification while sending credentials, tokens, and file contents.

Mitigation: Remove the lines that set check_hostname to False and verify_mode to CERT_NONE; use default verified TLS for Feishu API calls.

Risk: The workflow handles Feishu app secrets, tenant tokens, local file paths, and recipient IDs.

Mitigation: Keep app secrets outside source code, avoid logging tokens, and confirm the exact file path and recipient before uploading or sending a file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/swingmonkey/skills/feishu-file-transfer-guide)
- [Feishu Open Platform - Upload file](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/file/create)
- [Feishu Open Platform - Send message](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guide with PowerShell, Python, JSON, and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Feishu API endpoints and example credential placeholders; users supply real app credentials, file paths, and recipient IDs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
