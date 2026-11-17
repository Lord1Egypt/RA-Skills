## Description:

Convert any URL or file to Markdown. Supports webpage, WeChat, YouTube, Bilibili, Douyin, Xiaohongshu, PDF, and Office files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiwenai](https://clawhub.ai/user/haiwenai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert web pages, social media posts, videos, and local documents into Markdown for summarization, analysis, archival, or downstream document workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a third-party converter from a mutable GitHub source.

Mitigation: Review and pin the dependency before deployment, and run it in an isolated environment when possible.

Risk: YouTube conversions may retry with Chrome browser cookies.

Mitigation: Avoid sensitive browser profiles and confirm user consent before allowing browser cookie access.

## Reference(s):

- [anything-to-md homepage](https://github.com/haiwenai/anything-to-md)
- [ClawHub skill page](https://clawhub.ai/haiwenai/skills/anything-to-md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Guidance]

**Output Format:** [Markdown with YAML frontmatter; video conversions may include a timestamped transcript section.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write Markdown to stdout or a requested output path; requires python3 and ffmpeg, with optional yt-dlp, deno, and Whisper-related tooling for media inputs.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
