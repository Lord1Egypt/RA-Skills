## Description:

Use when the user wants to download a YouTube or Bilibili video by URL or title, saving to local Videos folder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzlupus](https://clawhub.ai/user/zzlupus)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to download YouTube or Bilibili videos by direct URL or title search into the local Videos folder.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to install yt-dlp without enough user review of the package source or installation method.

Mitigation: Require explicit user confirmation before installing software, and prefer a trusted package manager or a pinned, reviewed yt-dlp release.

Risk: Using browser cookies for login-required content can expose active authenticated sessions from the user's Chrome profile.

Mitigation: Use browser cookies only after explicit user consent, and prefer a dedicated browser profile or scoped cookie export for the target site.

Risk: The skill saves downloaded media to the local Videos folder, which can consume disk space or retrieve unintended playlist content.

Mitigation: Confirm the target URL or title, expected media scope, and destination folder before running playlist or large downloads.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces yt-dlp command guidance for video URLs, title search, format selection, subtitles, playlists, rate limits, and common troubleshooting.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
