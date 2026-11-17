## Description:

Search public Douyin videos, creator posts, comments, and trending topics, then return structured data and insights for creator discovery and content research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, content researchers, and analysts use this skill to find and compare creators, review public post performance and comments, and track Douyin trends for campaign planning and content research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and links are sent to the third-party Guaikei API.

Mitigation: Use a dedicated API token and submit only queries you are comfortable sharing with the provider.

Risk: Provider charges and privacy practices may affect use.

Mitigation: Check the provider's current pricing and privacy terms before making requests.

Risk: Most command results are saved as local logs.

Mitigation: Delete saved logs when they are no longer needed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/why20261/skills/douyin-kol-discovery)
- [Publisher profile](https://clawhub.ai/user/why20261)
- [Guaikei service and access](https://www.guaikei.com)
- [Command options](references/options.md)
- [Comment analysis guide](references/demand-mining.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON results with concise Markdown summaries and insights]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and retrieval filters control the result set. Most command results are saved locally, and some media links expire.]

## Skill Version(s):

1.4.2 (source: frontmatter, package.json, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
