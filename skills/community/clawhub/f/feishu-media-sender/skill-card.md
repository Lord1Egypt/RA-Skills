## Description: <br>
Feishu Media Sender uploads and sends images or videos through Feishu OpenAPI with in-chat preview or playback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinranphoto](https://clawhub.ai/user/yinranphoto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send local image or video files to Feishu chats from an agent workflow. It is intended for Feishu bot workflows that need media upload and message delivery through configured OpenClaw credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a selected local image or video file through a configured Feishu app. <br>
Mitigation: Confirm the file path and recipient ID before running the command, and use credentials scoped to the intended bot and workspace. <br>
Risk: The skill reads Feishu app credentials from ~/.openclaw/openclaw.json at runtime. <br>
Mitigation: Limit access to the OpenClaw config file and rotate credentials if they are exposed or no longer needed. <br>


## Reference(s): <br>
- [Feishu Upload Image API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/image/create) <br>
- [Feishu Upload File API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/file/create) <br>
- [Feishu Send Message API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create) <br>
- [ClawHub Skill Page](https://clawhub.ai/yinranphoto/feishu-media-sender) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Guidance] <br>
**Output Format:** [Text and JSON response output from the Feishu send operation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, Feishu network access, a local media file path, and OpenClaw Feishu credentials in ~/.openclaw/openclaw.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
