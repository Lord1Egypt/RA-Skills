## Description: <br>
Generates Alibaba Cloud DashScope and LingMou media workflows for talking-head video, full-body animation, text-to-image, image-to-video, text-to-speech, and template-based digital-human videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and media automation users use this skill to choose and run Alibaba Cloud avatar, speech, image, and video generation pipelines. It helps prepare required credentials, select the right script, upload local media when needed, and download generated media outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles cloud credentials for DashScope, Alibaba Cloud AccessKey, OSS, and LingMou operations. <br>
Mitigation: Use a dedicated least-privilege RAM user or role, avoid root credentials, and rotate keys regularly. <br>
Risk: The skill uploads user media to OSS and sends media URLs to Alibaba Cloud generation services. <br>
Mitigation: Use a temporary bucket or restricted prefix, keep signed URL lifetimes short, and delete uploaded and generated personal media after use. <br>
Risk: Environment-selected API hosts can receive credentials if DASHSCOPE_BASE_URL or LINGMOU_ENDPOINT is pointed at an untrusted host. <br>
Mitigation: Do not override those endpoint variables unless the destination is fully trusted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sdk-team/alibabacloud-avatar-video) <br>
- [LivePortrait API](https://help.aliyun.com/zh/model-studio/liveportrait-api) <br>
- [Text-to-image API](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference) <br>
- [Image-to-video API](https://help.aliyun.com/zh/model-studio/image-to-video-api-reference/) <br>
- [Qwen TTS API](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime) <br>
- [AnimateAnyone API reference](references/aa-api.md) <br>
- [EMO API reference](references/emo-api.md) <br>
- [LingMou API reference](references/lingmou-api.md) <br>
- [OSS upload reference](references/oss-upload.md) <br>
- [RAM permission policies](references/ram-policies.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and script parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or download generated images, audio, and video files through the referenced scripts.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
