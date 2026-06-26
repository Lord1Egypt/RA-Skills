## Description: <br>
抖音无水印视频下载和文案提取工具，可从抖音分享链接获取无水印视频下载链接、下载视频、提取视频语音文案并保存到文件。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuaixiaohao](https://clawhub.ai/user/shuaixiaohao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content-processing agents use this skill to inspect Douyin share links, download no-watermark video files, and generate transcript Markdown from video audio. It is intended for workflows where the user has rights to process the referenced content and can provide a SiliconFlow API key for transcription. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video audio is sent to SiliconFlow for transcription. <br>
Mitigation: Process only content the user has rights to handle, avoid sensitive media unless approved, and review SiliconFlow data-handling requirements before use. <br>
Risk: Downloaded videos and generated transcripts are saved locally. <br>
Mitigation: Use a controlled output directory, restrict file access as needed, and delete generated media or transcripts when they are no longer required. <br>
Risk: URL validation and download size limits are not enforced by the skill. <br>
Mitigation: Use trusted Douyin links and run the downloader in a restricted environment when processing untrusted input. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shuaixiaohao/douyin-video-transcript) <br>
- [SiliconFlow Console](https://cloud.siliconflow.cn/) <br>
- [SiliconFlow Audio Transcriptions API](https://api.siliconflow.cn/v1/audio/transcriptions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Python snippets; runtime outputs include video files and transcript Markdown files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FFmpeg, Python dependencies, and a SiliconFlow API key for transcription.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
