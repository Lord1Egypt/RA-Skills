## Description: <br>
Byted Kickart Video Subtitler helps an agent upload a video, prepare subtitle timing data, and submit a Volcengine/Kickart job that embeds captions into the video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to add subtitles to MP4 or MOV videos through Volcengine/Kickart services. The agent guides credential checks, package validation, video upload, subtitle JSON preparation, user confirmation, and result retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive Volcengine credentials and the security summary notes that credentials may be requested in chat and authorization data may be logged. <br>
Mitigation: Use scoped or isolated credentials, avoid long-lived AK/SK secrets in chat, and verify that logs redact authorization data before use. <br>
Risk: The skill uploads user videos, captions, and generated outputs to Bytedance/Volcengine/Kickart services. <br>
Mitigation: Use it only when users have consented to remote processing and avoid submitting confidential, regulated, or unnecessary personal media. <br>
Risk: The skill can perform account package checks and update flows, and the security guidance calls out review of update install commands. <br>
Mitigation: Review package or billing-impacting actions and any proposed install command before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/volcengine-skills/byted-kickart-video-subtitler) <br>
- [Volcengine Kickart package console](https://console.volcengine.com/kickart/fusion/setting/combobuy?tab=combo) <br>
- [Volcengine IAM key management](https://console.volcengine.com/iam/keymanage) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON subtitle configuration files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces JSON result files and video preview URLs; requires remote media upload and Volcengine/Kickart credentials.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
