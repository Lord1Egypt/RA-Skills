## Description:

A Douyin research assistant that searches public videos and posts, retrieves trending topics, creator posts, individual post details, and comments, and returns structured results for analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Content teams and analysts can use the skill to find Douyin content, follow public trends and creator activity, inspect individual posts, and summarize public comments for content and market research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan flags a mismatch between the advertised daily likes-growth ranking and reported search and hot-search behavior; some code was only partially inspected.

Mitigation: Review whether the reported features match the intended use and whether the available scan evidence is sufficient before installing.

Risk: The skill sends user-provided keywords and Douyin links to the third-party Guaikei API.

Mitigation: Use only keywords and links that are appropriate to share with that service; avoid including sensitive information.

## Reference(s):

- [Skill instructions and command guide](SKILL.md)
- [Query options](references/options.md)
- [Comment analysis guidance](references/demand-mining.md)
- [Release history](references/changelog.md)
- [Guaikei API service](https://www.guaikei.com)
- [ClawHub listing](https://clawhub.ai/why20261/skills/douyin-daily-surge)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON query results with concise text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the third-party API. Query limits vary by plan: up to 10,000 for usage-based tokens, 30 for monthly-token searches and creator posts, and 50 for comments.]

## Skill Version(s):

1.4.2 (source: frontmatter, package.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
