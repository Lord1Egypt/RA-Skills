## Description:

Use Alibaba Cloud DashScope API and LingMou workflows to guide agents through avatar video, image, video, and speech generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative operators use this skill to choose and run Alibaba Cloud media workflows for talking-head video, full-body animation, text-to-image, image-to-video, text-to-speech, and template-based digital-human broadcasts.

### Deployment Geography for Use:

Global, subject to Alibaba Cloud service availability for the documented cn-beijing and Singapore workflows.

## Known Risks and Mitigations:

Risk: The workflows can send selected media, prompts, scripts, and cloud credentials through Alibaba Cloud services.

Mitigation: Use least-privilege temporary credentials and run only with media and prompts approved for the configured Alibaba Cloud account.

Risk: Endpoint environment variables can influence where cloud requests are sent.

Mitigation: Verify that endpoint variables resolve to official Alibaba Cloud hosts before execution.

Risk: Signed media URLs and downloaded outputs can expose sensitive personal media if handled casually.

Mitigation: Avoid sensitive personal media unless provider handling and signed URL exposure are acceptable, and apply short retention or lifecycle cleanup for temporary assets.

Risk: Download mode has weak host allowlisting and bounded-download safeguards.

Mitigation: Use download mode cautiously, inspect generated URLs before fetching, and prefer controlled output locations.

## Reference(s):

- [LivePortrait API](https://help.aliyun.com/zh/model-studio/liveportrait-api)
- [Text-to-Image API](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)
- [Image-to-Video API](https://help.aliyun.com/zh/model-studio/image-to-video-api-reference/)
- [Qwen TTS Realtime](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime)
- [AA API Reference](references/aa-api.md)
- [EMO API Reference](references/emo-api.md)
- [LingMou API Reference](references/lingmou-api.md)
- [OSS Upload Reference](references/oss-upload.md)
- [RAM Permission Policies](references/ram-policies.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, code examples, and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or download media files when users run the referenced scripts with cloud credentials.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
