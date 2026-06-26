## Description: <br>
Downloads watermark-free Douyin videos on Windows and extracts spoken captions with local Whisper and optional semantic segmentation. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[openclawzhangchong](https://clawhub.ai/user/openclawzhangchong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Command-line users on Windows use this skill to inspect Douyin share links, download videos, and create transcript Markdown from video speech for personal learning or research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transcript text can be sent to MiniMax for semantic segmentation when segmentation is enabled and MINIMAX_API_KEY is set. <br>
Mitigation: Use --no-segment for local-only transcription, and only enable segmentation when sending transcript text to MiniMax is acceptable. <br>
Risk: The skill contacts Douyin to retrieve video information and downloads media from parsed links. <br>
Mitigation: Review before installing, use it only for links you are authorized to process, and follow the source platform's rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openclawzhangchong/douyindownloadwhisper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands] <br>
**Output Format:** [Command-line output plus saved video files and transcript Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, ffmpeg, local Whisper, and optional MiniMax API credentials for segmentation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
