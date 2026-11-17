## Description:

Fetches transcripts from YouTube and Bilibili videos so an agent can summarize video content, answer questions about it, or extract information from it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[donnycui](https://clawhub.ai/user/donnycui)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to retrieve plain-text subtitles from supported YouTube and Bilibili video URLs for downstream summarization, question answering, and content extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes yt-dlp against user-supplied video URLs and the security evidence notes weak URL scoping.

Mitigation: Use it only with trusted video URLs and review the URL before execution.

Risk: The security evidence flags unpinned installation guidance for the external downloader dependency.

Mitigation: Install yt-dlp from a pinned, verified, least-privilege environment.

Risk: Browser-cookie access can expose account context if enabled outside the skill's default flow.

Mitigation: Avoid browser-cookie access unless it is intentionally required for a trusted video source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/donnycui/skills/bilibili-youtube-watcher)
- [Publisher profile](https://clawhub.ai/user/donnycui)
- [yt-dlp project](https://github.com/yt-dlp/yt-dlp)
- [Original youtube-watcher skill](https://clawhub.ai/Michaelgathara/youtube-watcher)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown-formatted transcript text with platform, language, and URL headers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires yt-dlp in PATH and a video with available subtitles or auto-generated captions.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; artifact metadata reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
