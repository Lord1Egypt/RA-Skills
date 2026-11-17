## Description:

Searches public Douyin videos, creators, comments, and trending topics, returning structured data for content and market analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and analysts use the skill to discover Douyin content and trends, review public creator activity and engagement, and summarize comments for content planning, competitor monitoring, and audience analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and Douyin links are sent to the external GuaiKei API using an API token; the provider's data retention was not verified.

Mitigation: Submit only inputs you are comfortable sharing, review provider pricing and data handling, and keep the API token private.

Risk: Query results are saved in local log files and may remain after analysis.

Mitigation: Protect the skill directory and delete saved logs when they are no longer needed.

## Reference(s):

- [Usage and options](artifact/references/options.md)
- [Comment analysis guidance](artifact/references/demand-mining.md)
- [Changelog](artifact/references/changelog.md)
- [GuaiKei service](https://www.guaikei.com)
- [ClawHub skill page](https://clawhub.ai/why20261/skills/douyin-crawler-guaikei)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON data and concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search, creator, comment, detail, and trend results; query results are also saved locally for later review.]

## Skill Version(s):

1.4.2 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
