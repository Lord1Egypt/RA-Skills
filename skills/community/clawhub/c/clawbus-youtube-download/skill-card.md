## Description:

Downloads YouTube videos, playlists, audio, thumbnails, metadata, and subtitles with yt-dlp, including format selection, local saves, cookies for restricted videos, resumed downloads, and yt-dlp installation or updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawbus](https://clawhub.ai/user/clawbus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external users use this skill to download YouTube media through yt-dlp while choosing output location, formats, audio extraction, subtitles, thumbnails, cookies, and additional yt-dlp options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can install or update yt-dlp in the user's Python environment during normal use.

Mitigation: Preinstall a trusted pinned yt-dlp version and run the helper with `--skip-update` when automatic dependency changes are not acceptable.

Risk: The helper can use browser cookies for authenticated or restricted videos.

Mitigation: Avoid `--cookies-from-browser` unless authenticated access is required and the runtime handling browser session cookies is trusted.

Risk: Downloading media may create copyright or permission issues.

Mitigation: Use the skill only for media the user has rights or permission to download.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Files, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and local downloaded media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create files under a local output directory and may pass through user-supplied yt-dlp options.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
