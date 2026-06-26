## Description: <br>
抖音无水印视频下载和文案提取工具 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whille](https://clawhub.ai/user/whille) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to inspect Douyin share links, download watermark-free videos, and extract transcript text from video audio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transcript text may be sent to MiniMax for semantic segmentation even though user documentation describes segmentation as using OpenClaw's built-in LLM. <br>
Mitigation: Review before installing; use --no-segment or leave MINIMAX_API_KEY unset to avoid MiniMax segmentation until the remote data flow is documented. <br>
Risk: Audio from downloaded videos is sent to SiliconFlow for transcription, which may expose private, confidential, regulated, or copyrighted content. <br>
Mitigation: Use extraction only for videos and audio you are permitted and comfortable sending to SiliconFlow; avoid processing sensitive or regulated material. <br>
Risk: The security guidance notes incomplete documentation for MiniMax, curl usage, exact output paths, and remote data flows. <br>
Mitigation: Treat the skill as requiring review before deployment and document these behaviors before relying on it in a shared or production environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whille/douyin-download) <br>
- [SiliconFlow API key portal](https://cloud.siliconflow.cn/) <br>
- [SiliconFlow audio transcription endpoint](https://api.siliconflow.cn/v1/audio/transcriptions) <br>
- [MiniMax API endpoint](https://api.minimaxi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files] <br>
**Output Format:** [Console text plus downloaded media files and Markdown transcript files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ffmpeg and SILI_FLOW_API_KEY for transcription; MiniMax segmentation is controlled by MINIMAX_API_KEY and can be skipped with --no-segment.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
