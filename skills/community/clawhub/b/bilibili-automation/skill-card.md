## Description:

Automates Bilibili video search, playback, subtitle or danmaku extraction, video information retrieval, and summarization through BrowserWing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxsuki](https://clawhub.ai/user/maxsuki)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to automate common Bilibili workflows, including finding videos, extracting subtitles or danmaku, retrieving video metadata, and summarizing video content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, video URLs, subtitles, and account-linked content may be sent to the configured BrowserWing endpoint.

Mitigation: Use only a trusted BrowserWing endpoint and avoid sending sensitive or private Bilibili content.

Risk: Optional Bilibili cookies can expose account access if mishandled.

Mitigation: Configure cookies only when required, store them as secrets, and rotate or remove them after use.

Risk: The documented curl examples can become unsafe if raw user input is interpolated into shell commands.

Mitigation: Serialize request JSON safely and invoke commands without shell interpolation when adapting the examples.

Risk: Automated requests may violate Bilibili usage rules or trigger rate limits.

Mitigation: Use conservative request spacing, respect platform terms, and avoid bulk or unauthorized activity.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maxsuki/skills/bilibili-automation)
- [Bilibili](https://www.bilibili.com)
- [BrowserWing API documentation](http://localhost:8080/docs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return Bilibili search results, subtitles, danmaku, video metadata, and concise summaries.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
