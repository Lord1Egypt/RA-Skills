## Description: <br>
Use when the user wants to download a YouTube or Bilibili video by URL or title, saving to local Videos folder. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zzlupus](https://clawhub.ai/user/zzlupus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to prepare yt-dlp commands for downloading YouTube or Bilibili videos by URL or title into the local Videos folder. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to install and run yt-dlp downloads on the user's machine. <br>
Mitigation: Require user approval before package installation or downloads, and confirm playlist downloads before execution. <br>
Risk: The skill includes optional cookie-based Bilibili access that can use a browser login session. <br>
Mitigation: Avoid --cookies-from-browser unless the user understands the login-session exposure; prefer a dedicated browser profile or limited cookies file. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include package installation guidance and yt-dlp command options for video, audio, subtitles, playlists, and rate limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
