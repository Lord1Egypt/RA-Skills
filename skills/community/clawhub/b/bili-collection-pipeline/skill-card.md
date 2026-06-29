## Description: <br>
Batch-transcribes Bilibili collections and YouTube playlists into semantically segmented Markdown using local download, audio extraction, and Whisper transcription tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaozishan](https://clawhub.ai/user/xiaozishan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content-processing teams use this skill to turn Bilibili collections or YouTube playlists into local transcript files and segmented Markdown knowledge-base material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow contacts Bilibili and YouTube, invokes local media tools, and downloads media into the local workspace. <br>
Mitigation: Run it in a dedicated workspace, review playlist URLs first, and confirm you have adequate disk space and rights to process the media. <br>
Risk: Dependency and local tooling behavior can change across faster-whisper, requests, you-get, yt-dlp, and ffmpeg versions. <br>
Mitigation: Update or pin dependencies and external tools before use, then test on a small collection before processing large batches. <br>
Risk: Optional external LLM cleanup can send transcript content to an external provider if configured by the user. <br>
Mitigation: Use optional external LLM cleanup only when transcript content is safe to send to that provider, or keep post-processing local. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaozishan/skills/bili-collection-pipeline) <br>
- [you-get](https://github.com/soimort/you-get) <br>
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) <br>
- [FFmpeg](https://ffmpeg.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated artifacts include collection JSON, progress JSON, and Markdown transcript files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local media-derived transcript files and may use CUDA or CPU Whisper inference depending on command options.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
