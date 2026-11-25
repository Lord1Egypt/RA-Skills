## Description:

This skill retrieves public Douyin search, trending, creator-post, video-detail, and comment data through Guaikei and returns structured results for content research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Content, marketing, and data analysts use the skill to find public Douyin videos and creators, follow trends, and review public engagement for content planning, competitor research, and sentiment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and supplied Douyin links or IDs may be sent to www.guaikei.com, and API access requires a GUAIKEI_API_TOKEN.

Mitigation: Review query terms and links before each lookup, avoid sending sensitive information, and keep the token in the environment rather than placing it in commands or shared output.

Risk: The security scan was partial and reports medium confidence, so its benign verdict does not establish that every artifact file was fully inspected.

Mitigation: Review the skill files and requested account-search or post-detail features before installation, especially if they are outside the intended use.

## Reference(s):

- [Guaikei service and token access](https://www.guaikei.com)
- [Usage guide and command examples](readme.md)
- [Output contract](references/contract.md)
- [Command options](references/options.md)
- [Errors and retry guidance](references/errors.md)
- [Demand analysis guide](references/demand-mining.md)
- [Customer acquisition guide](references/customer-acquisition.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Markdown, Tables]

**Output Format:** [Structured JSON results with concise text or Markdown summaries and analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public video, creator, engagement, trend, and comment data for follow-up analysis.]

## Skill Version(s):

1.5.0 (source: SKILL.md frontmatter, package.json, and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
