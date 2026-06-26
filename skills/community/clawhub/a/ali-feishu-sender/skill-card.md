## Description: <br>
Ali Feishu Sender helps an agent send text, images, audio, video, rich text, and interactive cards to Feishu/Lark users or groups through Feishu APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuan-huicheng](https://clawhub.ai/user/yuan-huicheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workflow builders use this skill to have an agent upload selected local or generated media and send it to Feishu/Lark recipients. It is suited for workflows that need formatted Feishu delivery of images, voice bubbles, inline video, rich text, or cards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected text or media may be uploaded to Feishu/Lark and delivered to the wrong recipient or group. <br>
Mitigation: Confirm the destination recipient or group before sending and avoid sending sensitive files unless the workflow explicitly requires it. <br>
Risk: Feishu app credentials can authorize uploads and messages if exposed or over-permissioned. <br>
Mitigation: Use least-privilege Feishu credentials, provide them through environment variables or a secure secret store, and rotate them if exposure is suspected. <br>
Risk: Media conversion can leave .opus, .mp4, or _fs.mp4 files next to the originals. <br>
Mitigation: Review generated media artifacts after use and remove temporary converted files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yuan-huicheng/ali-feishu-sender) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/yuan-huicheng) <br>
- [Feishu File Upload API Endpoint](https://open.feishu.cn/open-apis/im/v1/files) <br>
- [Feishu Image Upload API Endpoint](https://open.feishu.cn/open-apis/im/v1/images) <br>
- [Feishu Message API Endpoint](https://open.feishu.cn/open-apis/im/v1/messages) <br>
- [Feishu Tenant Access Token API Endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Python function calls, CLI commands, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uploads selected content to Feishu/Lark and may create converted media files such as .opus, .mp4, or _fs.mp4 next to source files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
