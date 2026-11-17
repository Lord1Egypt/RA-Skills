## Description:

提取抖音播放页音频并通过自建服务转写字幕，随后总结内容、重点、观点或行动项。用户发送 douyin.com 链接、抖音分享文案，或要求总结、转写抖音视频时使用；不处理用户上传的本地视频文件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruidongyuan-dot](https://clawhub.ai/user/ruidongyuan-dot)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to turn a Douyin link or share text into a transcript, summary, key points, notes, action items, or readable subtitles. It is intended for Douyin web links and does not process local video uploads or non-Douyin URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted Douyin page metadata could affect the documented shell command used to call the transcription script.

Mitigation: Use a shell-free process invocation or strict escaping and validation for metadata and URLs before execution.

Risk: Audio, metadata, and the API key are handled by external services for transcription, temporary storage, and billing.

Mitigation: Use only trusted Douyin links, store DOUYIN_API_KEY in a secure credential store, and avoid exposing signed media URLs or full keys in logs or responses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ruidongyuan-dot/skills/douyin-video-summary)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summary, notes, action items, or segmented transcript; the transcription helper emits JSON for agent processing.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include video title, author, duration, charge amount, timestamps, summaries, notes, action items, or subtitles; signed audio URLs and full API keys should not be exposed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
