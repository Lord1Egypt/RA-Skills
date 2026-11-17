## Description:

Provides keyword search, hot-list lookup, public creator-post retrieval, and comment analysis for Douyin videos and image posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

External users and content analysts use this skill to discover public Douyin posts, monitor trends, review creator content, and analyze comment activity for content planning and competitor research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Use requires a GuaiKei access token, and provider fees may apply.

Mitigation: Keep GUAIKEI_API_TOKEN private and review the provider’s fees before use.

Risk: Retrieved results remain in local logs until removed.

Mitigation: Review the logs/ directory and remove stored results when they are no longer needed.

## Reference(s):

- [GuaiKei service and access](https://www.guaikei.com)
- [Douyin](https://www.douyin.com)
- [Options reference](references/options.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Text]

**Output Format:** [Structured JSON results with concise text summaries when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include post URLs, author details, timestamps, and engagement metrics.]

## Skill Version(s):

1.4.0 (source: SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
