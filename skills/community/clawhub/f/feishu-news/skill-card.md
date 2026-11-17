## Description:

A skill to fetch and reference news information from Feishu when interacting with users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yeat](https://clawhub.ai/user/yeat)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to retrieve Feishu news items, format them for conversation, and preserve source attribution when referencing current news.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependencies are broader than the mock implementation requires and are not locked to exact versions.

Mitigation: Pin or lock dependencies before production deployment and remove unused packages while the skill remains mock-only.

Risk: Generic news requests may invoke Feishu when the user expected a different news source.

Mitigation: Clarify when Feishu should be used and ask for source preference when the requested source is ambiguous.

## Reference(s):

- [Feishu News Skill on ClawHub](https://clawhub.ai/yeat/skills/feishu-news)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-formatted news summaries with source attribution links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output depends on Feishu source availability and configured news sources.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
