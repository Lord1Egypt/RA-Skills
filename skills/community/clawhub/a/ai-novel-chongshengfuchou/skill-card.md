## Description:

生成给定题材的中文重生复仇爽文，将正文转换为语音，并用本地素材合成为竖屏短视频。

This skill is ready for commercial/non-commercial use.

## Publisher:

[h1456942763](https://clawhub.ai/user/h1456942763)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to automate a Chinese short-video workflow: generate a rebirth revenge story, synthesize narration, and combine narration, background video, and music into a 1080x1920 MP4.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video processing can execute unsafe shell commands from media filenames.

Mitigation: Review before installing, use only trusted media files in an isolated workspace, and fix the package to remove shell=True and validate media filenames before deployment.

Risk: Story text may be sent to both the configured OpenAI-compatible endpoint and a hardcoded third-party TTS service.

Mitigation: Do not place confidential text in output.txt; make the TTS endpoint configurable and clearly disclose all external services before use.

Risk: The security evidence marks the release verdict as suspicious.

Mitigation: Require a preflight review and explicit confirmation before running the full pipeline.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/h1456942763/skills/ai-novel-chongshengfuchou)
- [FFmpeg Download](https://ffmpeg.org/download.html)
- [Pexels Videos](https://www.pexels.com/videos/)
- [Pixabay Videos](https://pixabay.com/videos/)
- [Free Music Archive](https://freemusicarchive.org/)
- [YouTube Audio Library](https://www.youtube.com/audiolibrary)
- [Zero Libre TTS API Endpoint](https://zero-libre-tts.vercel.app/api/tts)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands; generated files include output.txt, audio/*.mp3, and output.mp4.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an OpenAI-compatible API key, FFmpeg/ffprobe, local video files, and bgm.mp3; story text may be sent to the configured LLM endpoint and the TTS service.]

## Skill Version(s):

1.0.2 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
