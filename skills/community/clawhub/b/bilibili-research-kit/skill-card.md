## Description:

Extract and analyze Bilibili video content using yt-dlp, including video metadata, danmaku, subtitles, UP owner profile information, and series or collection data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuya227939](https://clawhub.ai/user/xuya227939)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, content creators, and content analysts use this skill to extract structured Bilibili video, subtitle, danmaku, creator profile, and collection information for analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser cookies used for Bilibili authentication are sensitive account credentials and can be exposed if shared, logged, or used in shared environments.

Mitigation: Use cookie-based authentication only on the user's own machine and account, avoid sharing or logging cookies, and prefer an isolated Python environment with a pinned yt-dlp version.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuya227939/skills/bilibili-research-kit)
- [Publisher profile](https://clawhub.ai/user/xuya227939)
- [Support issues](https://github.com/xuya227939/bilibili-research-kit/issues)
- [SnapVee homepage](https://snapvee.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON field references, tables, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include yt-dlp, curl, and local parsing commands; cookie-based authentication guidance may apply when content requires login.]

## Skill Version(s):

1.0.0 (source: release evidence, SKILL.md body, and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
