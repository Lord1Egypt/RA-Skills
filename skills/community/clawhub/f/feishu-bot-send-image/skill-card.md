## Description: <br>
Send local image files as native Feishu image messages via the Feishu Bot API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JasonZhang2015](https://clawhub.ai/user/JasonZhang2015) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to send generated images, charts, screenshots, or other local image files directly into Feishu user or group chats as previewable image messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Feishu app secret can be exposed if passed directly in shell history, shared terminals, logs, or screenshots. <br>
Mitigation: Prefer a wrapper that reads the secret from a protected environment variable or local config file, and avoid displaying credentials in command history or logs. <br>
Risk: The selected image is uploaded to Feishu and sent as the configured bot to the requested recipient. <br>
Mitigation: Confirm the image path, recipient ID, and recipient ID type before execution, and keep the bot permissions limited to the required Feishu scopes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JasonZhang2015/feishu-bot-send-image) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu image upload API](https://open.feishu.cn/open-apis/im/v1/images) <br>
- [Feishu message send API](https://open.feishu.cn/open-apis/im/v1/messages) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Text] <br>
**Output Format:** [Shell script invocation with text status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uploads the selected local image to Feishu and sends it as the configured bot to a specified user or group recipient.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
