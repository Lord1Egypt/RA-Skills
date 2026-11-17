## Description:

Download videos, audio, playlists, subtitles, and thumbnails from ANY platform (YouTube, TikTok, Instagram, Facebook, Twitter/X, Twitch, Vimeo, SoundCloud, Reddit, and 1000+ more) using yt-dlp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcbaivn](https://clawhub.ai/user/mcbaivn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to download media, playlists, subtitles, and thumbnails from supported web platforms and optionally send small completed downloads to Telegram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloaded media may be sent to Telegram automatically when the file is under 50 MB.

Mitigation: Install and use the skill only when that transfer behavior is intended, and confirm where downloaded files will be sent before use.

Risk: Browser-cookie options can grant the agent access to a logged-in session for private or restricted content.

Mitigation: Avoid cookie-based downloads unless the user explicitly authorizes access to that browser session for the requested URL.

Risk: PowerShell command templates executed against untrusted URLs can have unintended file or network effects.

Mitigation: Review command templates and destination paths before execution, especially when handling untrusted URLs.

## Reference(s):

- [Download AIO command reference](references/commands.md)
- [Download AIO platform reference](references/platforms.md)
- [Download AIO troubleshooting reference](references/troubleshooting.md)
- [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)
- [ClawHub skill page](https://clawhub.ai/mcbaivn/skills/download-aio)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline PowerShell command blocks and file-handling guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May download local media files and may send files under 50 MB to Telegram when configured.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
