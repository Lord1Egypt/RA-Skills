## Description:

Bilibili Video Summarizer downloads available Bilibili subtitles, parses them into plain text, and helps an agent produce structured summaries in Chinese or English.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yeezi02](https://clawhub.ai/user/yeezi02)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to summarize Bilibili videos by downloading official or AI-generated subtitles, converting them to plain text, and drafting a concise structured summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide and persist a Bilibili SESSDATA login session cookie.

Mitigation: Use only in a trusted local environment, treat SESSDATA as a credential, store it with restrictive file permissions, and delete or revoke it after use.

Risk: The artifact recommends a system-level yt-dlp installation command.

Mitigation: Install yt-dlp in an isolated, pinned environment instead of using a broad system-level pip install.

Risk: Summaries depend on the availability and quality of official or AI-generated subtitles.

Mitigation: Tell users when subtitles are unavailable and keep generated summaries faithful to the retrieved subtitle text.

## Reference(s):

- [Bilibili Cookie Setup Guide](references/cookie-setup.md)
- [Bilibili](https://www.bilibili.com)
- [Bilibili Video Summarizer on ClawHub](https://clawhub.ai/yeezi02/skills/bilibili-video-summarizer)
- [Publisher Profile](https://clawhub.ai/user/yeezi02)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summary with extracted subtitle text and inline shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Bilibili SESSDATA cookie and yt-dlp to retrieve subtitles.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
