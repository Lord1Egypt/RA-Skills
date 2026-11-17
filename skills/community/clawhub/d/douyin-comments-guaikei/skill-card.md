## Description:

Retrieves and analyzes public Douyin search results, hot lists, creator posts, video details, and comments as structured data for trend, competitor, sentiment, and audience-need analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Social media analysts, content teams, and product operators use the agent to find public Douyin content and summarize audience feedback, trends, and competitor activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is benign but partial: 24 of 42 components were fully scanned, and some executable files were not fully interpreted.

Mitigation: Review the remaining executable components and environment access before installation; keep the API token private.

Risk: Search keywords and supplied Douyin links are sent to the GuaiKei third-party API.

Mitigation: Use public Douyin content and avoid submitting sensitive information; keep retrieved data within the documented personal or team analysis use.

## Reference(s):

- [Usage and parameter options](references/options.md)
- [Comment demand-mining guide](references/demand-mining.md)
- [Changelog](references/changelog.md)
- [GuaiKei service and token support](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Markdown]

**Output Format:** [Structured JSON with concise analysis in Markdown when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public Douyin content and engagement data; available result counts depend on the API plan.]

## Skill Version(s):

1.4.2 (source: server-resolved release, SKILL.md frontmatter, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
