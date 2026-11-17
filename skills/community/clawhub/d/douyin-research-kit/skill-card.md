## Description:

Extract and analyze Douyin content using yt-dlp, including video metadata, captions, creator profiles, music or sound information, hashtags, live stream information, and engagement stats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuya227939](https://clawhub.ai/user/xuya227939)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and content researchers use this skill to extract structured Douyin data from videos, profiles, music pages, hashtags, and live streams and present the results as research-ready summaries or tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser cookies can expose an authenticated Douyin session when passed to yt-dlp.

Mitigation: Try unauthenticated extraction first; if cookies are required, get explicit user consent and use a dedicated browser profile with only the needed Douyin session.

Risk: The skill relies on local yt-dlp execution.

Mitigation: Install yt-dlp from a trusted, pinned source and review commands before running them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuya227939/skills/douyin-research-kit)
- [SnapVee homepage](https://snapvee.com)
- [Support issues](https://github.com/xuya227939/douyin-research-kit/issues)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with yt-dlp shell commands, JSON field mappings, subtitles or captions, and formatted research tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference browser cookies and locally generated subtitle files when Douyin access controls require authenticated extraction.]

## Skill Version(s):

1.0.0 (source: release metadata and artifact/clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
