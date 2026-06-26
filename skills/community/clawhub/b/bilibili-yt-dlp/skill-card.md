## Description: <br>
使用 yt-dlp 和 ffmpeg 下载哔哩哔哩视频。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xbos1314](https://clawhub.ai/user/xbos1314) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agents use this skill to prepare yt-dlp and ffmpeg commands for downloading Bilibili videos, selecting formats, merging audio and video streams, and saving the result locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to run yt-dlp and ffmpeg and write downloaded video files locally. <br>
Mitigation: Approve the exact download command and output path before execution, and confirm whether the resulting file should be retained or deleted. <br>
Risk: Authenticated downloads may expose browser cookies or a cookie file to command-line tools. <br>
Mitigation: Avoid cookie authentication for public videos; when login is required, explicitly approve the browser profile or cookie file before use. <br>
Risk: The release security summary notes under-scoped cleanup behavior for downloaded files. <br>
Mitigation: Tell the agent where files should be stored and whether to delete them after delivery. <br>


## Reference(s): <br>
- [FFmpeg download documentation](https://ffmpeg.org/download.html) <br>
- [ClawHub skill page](https://clawhub.ai/xbos1314/bilibili-yt-dlp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide local browser use, cookie selection, output paths, and cleanup of downloaded video files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
