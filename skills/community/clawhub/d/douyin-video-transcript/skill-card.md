## Description:

从抖音分享链接解析无水印视频下载地址，下载视频，并可使用硅基流动语音识别提取视频文案保存为 Markdown 文件。

This skill is for research and development only.

## Publisher:

[shuaixiaohao](https://clawhub.ai/user/shuaixiaohao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to inspect Douyin share links, download watermark-free videos, and extract spoken video copy into saved transcript files. The artifact states it is intended for learning and research use and should not be used for copyright infringement or unlawful activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make unvalidated outbound requests from user-provided Douyin links and retrieved video URLs.

Mitigation: Run it in an isolated environment, use only trusted Douyin links, and add domain allowlists, request timeouts, and size limits before regular use.

Risk: Audio extracted from videos is uploaded to a remote transcription service.

Mitigation: Do not transcribe sensitive, private, copyrighted, or otherwise restricted audio unless the user has the necessary rights and is comfortable sending it to SiliconFlow.

Risk: The release depends on runtime packages and FFmpeg behavior that are not pinned by the artifact documentation.

Mitigation: Pin and scan dependencies, verify FFmpeg installation from trusted sources, and review the script before installing or executing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shuaixiaohao/skills/douyin-video-transcript)
- [SiliconFlow Cloud](https://cloud.siliconflow.cn/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Console text, Python return dictionaries, shell command examples, optional MP4 files, and Markdown transcript files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcript output is organized by video ID; extraction requires an API key and FFmpeg.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
