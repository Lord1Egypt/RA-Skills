## Description: <br>
Downloads videos, playlists, subtitles, and audio from YouTube, Bilibili, Twitter/X, TikTok, Vimeo, Instagram, Twitch, and other yt-dlp-supported sites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[feiskyer](https://clawhub.ai/user/feiskyer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill when they need an agent to save online videos, download playlists, select quality, extract MP3 audio, or include subtitles through yt-dlp. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser-cookie options can expose a logged-in browser session to yt-dlp for authenticated or age-restricted downloads. <br>
Mitigation: Use browser-cookie options only after explicit user consent for the specific URL and browser profile; avoid cookies for public videos. <br>
Risk: The skill can download media that the user may not be authorized to copy or retain. <br>
Mitigation: Use it only for content the user is authorized to download and follow applicable platform, rights-holder, and legal requirements. <br>
Risk: The bundled script runs yt-dlp and writes media files to a local output directory. <br>
Mitigation: Review the command before execution, keep yt-dlp updated, and choose an output directory that will not overwrite important files. <br>


## Reference(s): <br>
- [Platform-Specific Tips](references/platform-tips.md) <br>
- [ClawHub skill page](https://clawhub.ai/feiskyer/feiskyer-download-video) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline bash commands; successful runs create local video, audio, or subtitle files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default downloads go to ~/Downloads/Videos unless the user provides another output directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
