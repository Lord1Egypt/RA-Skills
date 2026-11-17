## Description:

Retrieves public Douyin search results, creator posts, video details, comments, and trending topics as structured data for content and audience analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and analysts can retrieve public Douyin videos, creator posts, post details, comments, and trending topics for topic discovery, competitor monitoring, and audience analysis. The skill returns structured data that an agent can summarize into reports or comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and links are sent to the GUAIKEI third-party service, which was not audited in the security evidence.

Mitigation: Use a dedicated token, send only queries you are comfortable sharing, and check the provider's privacy and pricing terms first.

Risk: Local logs can retain queries and retrieved public profile or comment data.

Mitigation: Periodically review and remove local logs that are no longer needed.

## Reference(s):

- [GUAIKEI service and access](https://www.guaikei.com)
- [Usage options](references/options.md)
- [Demand mining guide](references/demand-mining.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Text, Markdown]

**Output Format:** [Structured JSON data, with concise text or Markdown summaries and reports when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retrieves public Douyin data. Requires a GUAIKEI_API_TOKEN; result counts depend on the subscription plan, and returned links may expire.]

## Skill Version(s):

1.4.2 (source: server release evidence, skill frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
