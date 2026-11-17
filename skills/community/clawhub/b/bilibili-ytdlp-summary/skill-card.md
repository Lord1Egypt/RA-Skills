## Description:

当用户提供 B 站视频链接、BV 号或 b23.tv 短链，使用 yt-dlp 下载音频 + 硅基流动 ASR 转写，优先尝试官方字幕。支持 QQbot 自动推送。需要 node、yt-dlp 和 SILICONFLOW_API_KEY。

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaa-ljpcoder](https://clawhub.ai/user/aaa-ljpcoder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to turn Bilibili videos, BV identifiers, or b23.tv short links into transcripts and concise summaries. It prefers official subtitles when available, otherwise it downloads audio with yt-dlp and uses SiliconFlow ASR when an API key is configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted or non-Bilibili URL could cause unsafe command execution or network access outside the skill's intended behavior.

Mitigation: Use only trusted Bilibili, BV, or b23.tv inputs until URL handling is fixed, and avoid untrusted or user-supplied links.

Risk: When official subtitles are unavailable, audio may be sent to SiliconFlow for ASR.

Mitigation: Do not process sensitive or private video audio unless sending it to SiliconFlow is acceptable for the deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaa-ljpcoder/skills/bilibili-ytdlp-summary)
- [SiliconFlow API key management](https://cloud.siliconflow.cn/me/account/ak)
- [yt-dlp project](https://github.com/yt-dlp/yt-dlp)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text, JSON metadata, and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes summary.md, transcript.txt, probe_result.json, and transcription_result.json; downloaded audio is deleted after transcription when cleanup succeeds.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
