## Description: <br>
Send text, markdown, images, and files to Feishu (Lark) chats through the Feishu Open API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhendexuebuhui](https://clawhub.ai/user/zhendexuebuhui) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation agents use this skill to send notifications, reports, and selected local files or images to configured Feishu/Lark chats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu app credentials can authorize outbound messages and file uploads. <br>
Mitigation: Use least-privileged Feishu app credentials and protect FEISHU_APP_SECRET from logs, prompts, and shared files. <br>
Risk: Selected message content or local files may contain sensitive information that will be sent to Feishu/Lark. <br>
Mitigation: Review message text and file paths before sending, and avoid passing sensitive content unless it is intended for the target chat. <br>
Risk: A misconfigured default chat ID can send content to the wrong Feishu/Lark chat. <br>
Mitigation: Verify FEISHU_CHAT_ID before use or pass an explicit chat ID for high-sensitivity sends. <br>


## Reference(s): <br>
- [Feishu Open Platform](https://open.feishu.cn/app) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Feishu/Lark chat messages, uploaded files or images, JSON-like API response data, and plain-text CLI status output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FEISHU_APP_ID, FEISHU_APP_SECRET, and FEISHU_CHAT_ID environment variables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
