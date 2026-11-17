## Description:

Download Bilibili videos after asking the user for a Bilibili URL, using a provided Python script that supports single-video and batch playlist downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caiyundc880518](https://clawhub.ai/user/caiyundc880518)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to download individual Bilibili videos or playlists through a Python wrapper around yt-dlp, with optional format selection and batch controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill does not enforce its claimed Bilibili-only scope before passing user input to yt-dlp.

Mitigation: Use only trusted Bilibili URLs, run downloads in a sandboxed download directory, and add strict Bilibili host validation plus a '--' separator before URLs.

Risk: Downloads can consume network bandwidth and local disk space, especially when batch playlist mode is enabled.

Mitigation: Set download size and directory limits before use, and require explicit user confirmation before enabling batch downloads.

Risk: An unpinned yt-dlp dependency can change downloader behavior over time.

Mitigation: Pin and periodically review the yt-dlp version used in managed deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caiyundc880518/skills/bililidownloader)
- [Publisher profile](https://clawhub.ai/user/caiyundc880518)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and downloader status text; downloaded media files are written by yt-dlp.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Bilibili URL, yt-dlp, Python 3.6 or newer, and ffmpeg for normal media handling.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
