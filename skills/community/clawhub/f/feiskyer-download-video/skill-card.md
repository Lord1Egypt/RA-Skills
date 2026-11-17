## Description:

Download videos and audio from supported websites such as YouTube, Bilibili, Twitter/X, TikTok, Vimeo, Instagram, and Twitch using yt-dlp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[feiskyer](https://clawhub.ai/user/feiskyer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare yt-dlp commands or run the bundled helper script for downloading videos, audio, subtitles, playlists, and selected formats from supported online video platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated downloads can use live browser session cookies, exposing logged-in sessions to yt-dlp or related downloader tooling.

Mitigation: Use cookie-based options only after explicit user intent, prefer unauthenticated downloads, and use a dedicated low-privilege browser profile when cookies are necessary.

Risk: Downloader dependencies and optional plugins may change behavior over time.

Mitigation: Install dependencies in an isolated environment and pin versions where practical.

Risk: The skill can download online media to local storage.

Mitigation: Use it only for media the user is authorized to download and confirm the destination directory before saving files.

## Reference(s):

- [Platform-Specific Tips](references/platform-tips.md)
- [ClawHub skill page](https://clawhub.ai/feiskyer/skills/feiskyer-download-video)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to run a local helper script or yt-dlp command that writes downloaded media files to a user-selected directory.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
