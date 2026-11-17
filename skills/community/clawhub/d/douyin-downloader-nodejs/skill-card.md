## Description:

抖音无水印视频下载和文案提取工具。

This skill is ready for commercial/non-commercial use.

## Publisher:

[whille](https://clawhub.ai/user/whille)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to fetch Douyin video information, download no-watermark videos locally, and optionally extract spoken transcript text through SiliconFlow transcription.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transcript extraction sends extracted audio to SiliconFlow for transcription.

Mitigation: Use extract mode only when the video audio can be shared with SiliconFlow under the user's data-handling requirements.

Risk: Weak URL validation may allow non-Douyin URLs to be passed to the downloader.

Mitigation: Pass only trusted Douyin share links until hostname validation is tightened.

Risk: The tool can read a generic API_KEY environment variable.

Mitigation: Prefer DOUYIN_API_KEY and avoid running the skill in environments that expose unrelated API_KEY secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whille/skills/douyin-downloader-nodejs)
- [SiliconFlow API key portal](https://cloud.siliconflow.cn/)
- [SiliconFlow audio transcription endpoint](https://api.siliconflow.cn/v1/audio/transcriptions)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [CLI stdout plus downloaded MP4 files and transcript Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ffmpeg for audio extraction; transcript extraction sends extracted audio to SiliconFlow and uses DOUYIN_API_KEY or API_KEY.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
