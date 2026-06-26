## Description: <br>
抖音无水印视频下载和文案提取工具 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whille](https://clawhub.ai/user/whille) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to inspect Douyin share links, download watermark-free video files, extract audio transcripts, and optionally format transcripts into semantic Markdown sections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio is sent to Silicon Flow for transcription when extraction is used. <br>
Mitigation: Use extraction only for videos whose audio may be shared with that external service, and set SILI_FLOW_API_KEY only when transcription is intended. <br>
Risk: Transcript text may be sent to MiniMax for semantic segmentation when MINIMAX_API_KEY is available. <br>
Mitigation: Unset MINIMAX_API_KEY or run extraction with --no-segment when transcript text should not be shared with MiniMax. <br>
Risk: The security scan verdict is suspicious because transcript sharing is under-disclosed. <br>
Mitigation: Review the skill and its external service disclosures before installation or deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whille/douyin-download-v2) <br>
- [Publisher profile](https://clawhub.ai/user/whille) <br>
- [Silicon Flow console](https://cloud.siliconflow.cn/) <br>
- [Silicon Flow transcription API](https://api.siliconflow.cn/v1/audio/transcriptions) <br>
- [MiniMax API endpoint](https://api.minimaxi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration] <br>
**Output Format:** [Console text plus optional downloaded MP4 files and transcript.md Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ffmpeg and SILI_FLOW_API_KEY for transcription; MINIMAX_API_KEY enables optional semantic segmentation unless --no-segment is used.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
