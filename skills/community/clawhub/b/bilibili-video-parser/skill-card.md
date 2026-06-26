## Description: <br>
下载并解析B站视频，用于需要理解视频视觉信息的单条B站视频分析任务。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielcy](https://clawhub.ai/user/danielcy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to resolve a Bilibili video link or BV ID, download the video with yt-dlp, and pass the local video to a video-analysis skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download remote video content and create local workspace files. <br>
Mitigation: Use explicit user-provided Bilibili links or BV IDs, review the target storage path before download, and remove retained video files when no longer needed. <br>
Risk: The skill depends on an external yt-dlp executable or YT_DLP_PATH setting. <br>
Mitigation: Install yt-dlp from a trusted source, verify the configured binary path, and stop if the expected command is unavailable. <br>
Risk: Remote videos may be untrusted or oversized. <br>
Mitigation: Avoid untrusted or unexpectedly large links and monitor workspace storage during download-heavy use. <br>


## Reference(s): <br>
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash command blocks and local video file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or reuse MP4 files under ./bilibili/videos and requires yt-dlp, optionally configured by YT_DLP_PATH.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
