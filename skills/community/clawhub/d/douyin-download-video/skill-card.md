## Description: <br>
Downloads videos from yt-dlp-supported sites such as YouTube, Bilibili, and Douyin using yt-dlp and FFmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heihu123](https://clawhub.ai/user/heihu123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when they want an agent to save videos or audio from yt-dlp-compatible sites into a local downloads folder, with options for quality, output directory, and audio-only extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically install or update local video-tool dependencies such as yt-dlp and FFmpeg. <br>
Mitigation: Use an isolated Python environment and prefer preinstalling pinned, verified versions of yt-dlp and FFmpeg before running the skill. <br>
Risk: Browser-cookie mode can expose authenticated browser sessions to download tooling. <br>
Mitigation: Use browser-cookie mode only for a specific intended site and session, and avoid it when downloading public or unauthenticated media. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/heihu123/douyin-download-video) <br>
- [FFmpeg downloads](https://ffmpeg.org/download.html) <br>
- [Windows FFmpeg build used by artifact](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python script usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a local Python helper that calls yt-dlp, writes downloaded media files to the selected output directory, and may install or locate video-tool dependencies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
