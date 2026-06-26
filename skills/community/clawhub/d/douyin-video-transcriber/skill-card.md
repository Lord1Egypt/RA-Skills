## Description: <br>
Transcribes one or more Douyin videos by downloading video media, extracting audio with ffmpeg, and running local Whisper speech-to-text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahsbnb](https://clawhub.ai/user/ahsbnb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and content operations teams can use this skill to convert Douyin video speech into text for review, content analysis, or copy extraction. It is intended for batch transcription workflows where the user supplies Douyin links and local runtime dependencies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a TikHub API token to download Douyin video data. <br>
Mitigation: Keep the token out of source control and logs, and provide it only through the supported local config or environment variable. <br>
Risk: The optional output-file path can overwrite files that the user account can write. <br>
Mitigation: Use a dedicated workspace output path and review the destination before running batch jobs. <br>
Risk: The release has no server-resolved GitHub import provenance. <br>
Mitigation: Verify the publisher and source before deployment, especially because the artifact text contains a placeholder repository URL. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ahsbnb/douyin-video-transcriber) <br>
- [Publisher profile](https://clawhub.ai/user/ahsbnb) <br>
- [ffmpeg downloads](https://ffmpeg.org/download.html) <br>
- [TikHub Douyin video API endpoint](https://api.tikhub.io/api/v1/douyin/web/fetch_one_video) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration guidance] <br>
**Output Format:** [Markdown transcription report plus a printed output path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The report contains one section per input video and may include per-video error details when processing fails.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
