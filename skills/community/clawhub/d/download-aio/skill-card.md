## Description: <br>
Download AIO helps an agent download videos, audio, playlists, subtitles, and thumbnails from supported media platforms with yt-dlp, then send files under 50 MB to Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcbaivn](https://clawhub.ai/user/mcbaivn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to download media, subtitles, thumbnails, or playlist items from supported public sites. It also supports authenticated downloads when the user explicitly chooses to use their own browser cookies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use browser cookies or cookies.txt for downloads that require a logged-in session. <br>
Mitigation: Use cookies only for the exact site and download the user explicitly authorizes, and avoid shared or sensitive browser sessions. <br>
Risk: Downloaded files under 50 MB may be sent to Telegram automatically. <br>
Mitigation: Confirm the destination and content before sending in sensitive environments, or require manual approval before Telegram transfer. <br>
Risk: Setup guidance references installer scripts that are not present in the release artifact. <br>
Mitigation: Review any installer script before running it, or install Python, yt-dlp, and ffmpeg manually from trusted sources. <br>


## Reference(s): <br>
- [Download AIO README](README.md) <br>
- [Download commands](references/commands.md) <br>
- [Supported platforms](references/platforms.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, files] <br>
**Output Format:** [Markdown with PowerShell command blocks, file attachments, or local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can send downloaded files to Telegram when they are 50 MB or smaller; larger files are reported by local path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
