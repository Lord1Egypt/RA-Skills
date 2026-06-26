## Description: <br>
飞书图片消息 helps an agent upload, send, retrieve, download, and view Feishu image messages using the bundled Python CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imBing](https://clawhub.ai/user/imBing) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to let an agent work with Feishu image messages, including uploading local images, sending image keys or files to chats, downloading images, and returning image data for inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HTTPS certificate and hostname verification are disabled while the script handles Feishu credentials, image content, and message sending. <br>
Mitigation: Review or patch the script to restore normal HTTPS verification before installing or running it. <br>
Risk: The skill can send images to Feishu chats or users, which can expose data if the recipient or image is wrong. <br>
Mitigation: Use least-privilege Feishu app scopes and confirm the recipient, chat type, and image before sending. <br>
Risk: The view command returns image contents as base64 data, which can expose sensitive images to the agent session. <br>
Mitigation: Avoid the view command for sensitive images and limit use to images approved for agent inspection. <br>
Risk: The download command can create directories and write files at the requested output path. <br>
Mitigation: Choose download paths carefully and run the skill with filesystem permissions limited to the intended workspace. <br>


## Reference(s): <br>
- [Feishu Upload Image API](https://open.feishu.cn/document/server-docs/im-v1/image/create) <br>
- [Feishu Get Image API](https://open.feishu.cn/document/server-docs/im-v1/image/get) <br>
- [Feishu Send Message API](https://open.feishu.cn/document/server-docs/im-v1/message/create) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, JSON, Files, Configuration] <br>
**Output Format:** [Markdown guidance with bash commands; the script prints JSON status objects, saved image files, or base64 image data URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials in the local OpenClaw configuration and Feishu scopes for image resources and bot message sending.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
