## Description: <br>
Uploads local or remote videos to Feishu and sends them as playable media messages with optional first-frame cover images and detected duration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vivila-yxx](https://clawhub.ai/user/vivila-yxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agents use this skill to send a selected local video file or downloaded remote video URL into the current Feishu chat. It is intended for Feishu messaging workflows that need in-chat video playback with uploaded media, optional cover images, and duration metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read a user-selected local video or fetch a remote video URL and send it to a caller-supplied Feishu destination. <br>
Mitigation: Use only with trusted publishers, explicit destinations, non-sensitive files, and user confirmation before sending externally. <br>
Risk: Recipient and source safeguards are not clearly enforced by the evidence. <br>
Mitigation: Prefer a release that restricts acceptable URLs, validates the Feishu recipient against the current chat, and prompts before external delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vivila-yxx/skills/feishu-video-message) <br>
- [Feishu Upload Image API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/image/create) <br>
- [Feishu Upload File API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/file/create) <br>
- [Feishu Send Message API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Files, Guidance] <br>
**Output Format:** [Command-line execution with Feishu API responses and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, ffmpeg, ffprobe, Feishu credentials in ~/.openclaw/openclaw.json, network access, and either a local video path or remote video URL plus an explicit receive-id.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
