## Description:

Queries Douyin public video and image-note data through keyword search, trending lists, creator posts, post details, and comments, returning structured results for content and competitor analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Content marketers, social media operators, and analysts use this skill to find Douyin videos and trends, review public creator posts and comments, and prepare topic, competitor, or audience-insight summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports medium confidence and partial file analysis, and notes a possible mismatch between the description and reviewed behavior.

Mitigation: Review the complete skill and compare its behavior with the stated capabilities before installation or use.

Risk: The skill sends user-provided search terms or Douyin links to the Guaikei third-party API and requires an API token.

Mitigation: Use only authorized public data, avoid submitting sensitive information, and keep GUAIKEI_API_TOKEN private.

## Reference(s):

- [Options reference](references/options.md)
- [Demand mining guide](references/demand-mining.md)
- [Guaikei API service](https://www.guaikei.com)
- [ClawHub release page](https://clawhub.ai/why20261/skills/douyin-kol-searchs)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON with concise text or Markdown analysis when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only queries of public Douyin data; result limits depend on the API plan.]

## Skill Version(s):

1.4.2 (source: SKILL.md frontmatter, package.json, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
