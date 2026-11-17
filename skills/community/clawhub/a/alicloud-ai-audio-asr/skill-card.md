## Description:

Transcribes non-realtime speech with Alibaba Cloud Model Studio Qwen ASR models for recorded audio, timestamped transcripts, and DashScope/OpenAI-compatible ASR request and response documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to transcribe recorded audio with Alibaba Cloud Qwen ASR, choose sync or async transcription flows, and save normalized transcript evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected audio files and the DashScope API key are sent to Alibaba Cloud during transcription.

Mitigation: Use non-sensitive test audio first, obtain consent before uploading private recordings, and handle DASHSCOPE_API_KEY as a secret.

Risk: The async helper can fetch a provider-returned transcription result URL.

Mitigation: Review or patch result URL fetching so it only follows expected Alibaba Cloud HTTPS result locations before using the skill with sensitive data.

## Reference(s):

- [Qwen ASR API Notes](references/api_reference.md)
- [Official Alibaba Cloud Qwen ASR Sources](references/sources.md)
- [Recorded speech recognition with Qwen](https://help.aliyun.com/zh/model-studio/recorded-speech-recognition-qwen)
- [Qwen ASR OpenAI-compatible API reference](https://help.aliyun.com/zh/model-studio/qwen-asr)
- [Qwen ASR file transcription API reference](https://help.aliyun.com/zh/model-studio/qwen-asr-filetrans-api)
- [ClawHub skill page](https://clawhub.ai/cinience/skills/alicloud-ai-audio-asr)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON transcript outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script writes normalized transcript JSON containing text, task status, task ID when present, and the raw provider response.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
