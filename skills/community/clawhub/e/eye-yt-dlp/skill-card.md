## Description:

Helps an agent use yt-dlp to download videos from YouTube, Bilibili, Twitter, Instagram, and other supported sites, using high-quality MP4 output by default.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frank-gith](https://clawhub.ai/user/frank-gith)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn a user-provided video URL into a concrete yt-dlp download command. It is intended for downloading requested media, with optional thumbnails or subtitles when the user asks for them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloads write media files to ~/Movies by default and may consume significant disk space.

Mitigation: Confirm the destination path and available disk space before running the generated yt-dlp command.

Risk: Playlist URLs can download more media than the user intended.

Mitigation: Confirm playlist downloads explicitly before using playlist-oriented options such as --yes-playlist.

Risk: Some sites may require cookies or account credentials, which can expose private session data.

Mitigation: Avoid using site cookies or account credentials unless necessary, and explain the privacy implications before doing so.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/frank-gith/skills/eye-yt-dlp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may create downloaded media files in ~/Movies by default when executed.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
