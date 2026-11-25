## Description:

Provides public Douyin search, creator, post, comment, and trending data for content research and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Content teams, brand researchers, and creators use this skill to explore Douyin posts and trends, compare creators or competitors, and summarize public comment themes for planning and monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries send supplied keywords and Douyin links or IDs to a third-party API.

Mitigation: Use only public content you intend to share, and avoid sending sensitive or private links or identifiers.

Risk: ClawScan reports medium confidence and incomplete scan coverage, and says some account-search behavior is not fully described.

Mitigation: Review the current capability and data-sharing disclosures before use if those details matter to you.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/why20261/skills/douyin-content-research-v1)
- [Douyin Content Research service and token portal](https://www.guaikei.com)
- [Output contract](references/contract.md)
- [Demand mining guide](references/demand-mining.md)
- [Customer acquisition guide](references/customer-acquisition.md)
- [Query options](references/options.md)
- [Error handling](references/errors.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Markdown]

**Output Format:** [Structured JSON query results with concise Markdown research summaries and tables when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public post, creator, trend, and comment data; results depend on the requested query and API access.]

## Skill Version(s):

1.5.0 (source: SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
