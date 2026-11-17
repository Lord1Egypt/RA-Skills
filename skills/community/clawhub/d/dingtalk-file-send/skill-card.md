## Description:

Upload and send files to DingTalk users. Auto-detects account from current session. Use when: user asks to send/forward a file/document/PDF/image via DingTalk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenriou](https://clawhub.ai/user/kenriou)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and agents use this skill to upload local files to DingTalk and send them to specified DingTalk users through a configured OpenClaw DingTalk account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically use local OpenClaw DingTalk credentials and upload selected local files to DingTalk.

Mitigation: Require explicit confirmation that shows the file path, recipient user ID, and resolved DingTalk account before upload or send.

Risk: Fallback account selection can send through an unintended DingTalk account when no binding is found.

Mitigation: Remove fallback account selection behavior or require the account binding to resolve before continuing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kenriou/skills/dingtalk-file-send)
- [DingTalk access token API](https://api.dingtalk.com/v1.0/oauth2/accessToken)
- [DingTalk media upload API](https://oapi.dingtalk.com/media/upload)
- [DingTalk robot message API](https://api.dingtalk.com/v1.0/robot/oToMessages/batchSend)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command examples for selecting a DingTalk account, uploading a file, sending the message, and checking delivery status.]

## Skill Version(s):

1.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
