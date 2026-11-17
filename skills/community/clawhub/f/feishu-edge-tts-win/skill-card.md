## Description:

飞书语音消息发送技能（Windows 版）。使用 Edge TTS（微软，免费）生成语音并以飞书语音气泡发送。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ztxdcyy](https://clawhub.ai/user/ztxdcyy)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill on Windows to convert provided text into a Chinese Edge TTS voice clip and send it to a Feishu user as an audio message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Feishu app credentials and can expose a bearer token locally during upload.

Mitigation: Review before installation, use least-privilege Feishu app credentials, and avoid sharing the configuration file beyond the local agent environment.

Risk: Input text is transmitted to Microsoft Edge TTS and the generated audio is transmitted to Feishu.

Mitigation: Do not send sensitive text unless the user accepts transmission to both services.

Risk: The upload path shells out to curl and depends on local ffmpeg and edge-tts behavior.

Mitigation: Prefer a revised version with an in-process HTTPS client, pinned dependencies, and verified local ffmpeg installation before operational use.

## Reference(s):

- [Feishu Open APIs](https://open.feishu.cn/open-apis)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Windows shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates temporary MP3 and OPUS audio, uploads the OPUS file to Feishu, and reports send status or a message_id.]

## Skill Version(s):

1.0.0 (source: release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
