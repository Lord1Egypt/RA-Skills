## Description: <br>
ffmpeg剪辑大师 helps agents edit local video and audio files with FFmpeg, including trimming, concatenation, transcoding, compression, subtitles, watermarks, screenshots, speed changes, GIF conversion, and audio processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[showtimewalker](https://clawhub.ai/user/showtimewalker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and media operators use this skill to have an agent run local FFmpeg workflows against selected audio and video files, then return structured output paths and processing details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local FFmpeg commands process user-selected media files and may overwrite existing output files. <br>
Mitigation: Use a dedicated OUTPUT_ROOT or unique output paths, and review selected input and output paths before execution. <br>
Risk: Local logs may record command details and file paths. <br>
Mitigation: Avoid sensitive file paths when possible and handle generated logs according to local data-handling rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/showtimewalker/ffmpeg-multimedia-editing) <br>
- [Publisher profile](https://clawhub.ai/user/showtimewalker) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and script JSON results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates local media outputs under OUTPUT_ROOT/outputs/ffmpeg/<operation>/ and JSON containing type, operation, paths, and elapsed seconds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
