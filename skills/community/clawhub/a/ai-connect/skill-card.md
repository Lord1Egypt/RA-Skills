## Description:

Ai Connect is an Agent Reach quick-reference skill that helps an agent read, search, and summarize content from major web and social platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smseow001](https://clawhub.ai/user/smseow001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to choose platform-specific commands for reading web pages, extracting video metadata or captions, searching social platforms, reading GitHub resources, and checking Agent Reach connectivity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated platform workflows may expose login cookies, which can enable account takeover if shared or logged.

Mitigation: Treat cookies like passwords: do not paste them into chat or logs, prefer OAuth or scoped tokens where available, restrict local cookie file permissions, and revoke sessions if exposure is suspected.

Risk: The skill invokes web-reading and platform-search tools whose retrieved content may be incomplete, unavailable, or platform-dependent.

Mitigation: Review extracted content and search results before relying on them, especially for external publication, business decisions, or authenticated account activity.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smseow001/skills/ai-connect)
- [Publisher profile](https://clawhub.ai/user/smseow001)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with inline shell commands and platform-specific examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require authenticated platform cookies for selected services; outputs can include extracted page text, video summaries, search results, and status checks.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
