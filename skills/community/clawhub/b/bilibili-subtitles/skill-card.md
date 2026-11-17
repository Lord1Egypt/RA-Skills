## Description:

Uses yt-dlp to extract existing uploaded or auto-generated subtitles from public Bilibili videos without downloading the full video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scottliu007](https://clawhub.ai/user/scottliu007)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to inspect Bilibili subtitle availability, download existing subtitle tracks, convert VTT subtitles to plain text, and use the text for summaries or question answering. It is limited to videos where Bilibili already provides subtitle tracks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using browser cookies or exported cookies.txt files can expose Bilibili account secrets.

Mitigation: Ask for explicit approval before cookie access, prefer a Bilibili-scoped cookies.txt file, avoid printing or pasting cookie contents, and delete exported cookie files after use.

Risk: The skill can return no usable content when a video has no uploaded or auto-generated subtitle track.

Mitigation: List available subtitles first and clearly report when no subtitle track exists instead of implying extraction succeeded.

Risk: Subtitle extraction may be inappropriate for content the user is not authorized to access or reuse.

Mitigation: Use the skill only for public or authorized content and follow applicable platform terms and copyright requirements.

## Reference(s):

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Bilibili subtitle troubleshooting reference](reference.md)

## Skill Output:

**Output Type(s):** [shell commands, guidance, text]

**Output Format:** [Markdown with inline bash commands and references to generated subtitle or plain-text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce .vtt, .srt, or plain-text subtitle files when commands are executed in the user's environment.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
