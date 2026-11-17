## Description:

使用本地Whisper模型识别飞书语音消息。离线免费，不需要注册，不需要联网。

This skill is ready for commercial/non-commercial use.

## Publisher:

[richardcoder849](https://clawhub.ai/user/richardcoder849)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to transcribe Feishu voice messages into text, with guidance for downloading voice audio, converting it to 16 kHz WAV, and running Whisper or cloud ASR services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill claims offline use, but the script can download Whisper models from a Hugging Face mirror.

Mitigation: Use a pinned, locally cached model and block unexpected network access when offline operation or reproducibility is required.

Risk: Voice messages may contain sensitive chat audio, and the README describes cloud ASR providers that may receive that audio.

Mitigation: Confirm privacy requirements before use, limit processing to approved audio, and use only Feishu and cloud credentials that are acceptable for the data involved.

Risk: Cloud and Feishu credentials are required for some documented workflows.

Mitigation: Grant least-privilege app permissions, store credentials outside skill files, and rotate them if exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/richardcoder849/skills/feishu-asr)
- [Hugging Face mirror endpoint](https://hf-mirror.com)
- [Alibaba Cloud ASR console](https://d.console.aliyun.com)
- [Tencent Cloud ASR](https://cloud.tencent.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples, plus transcription text when the script is run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May process local voice files and return recognized text; behavior depends on installed ASR dependencies and configured credentials.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
