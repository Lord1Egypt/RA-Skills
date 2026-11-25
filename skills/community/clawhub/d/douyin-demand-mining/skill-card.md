## Description:

Search public Douyin videos, creators, comments, and hot lists, then use the results to identify content trends, audience needs, and supporting examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

External users, marketers, and developers can search public Douyin content and creator accounts, inspect a post or its comments, and review structured results for content planning, audience research, trend monitoring, or competitor analysis. Comment guidance helps organize audience needs and pain points with supporting excerpts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries can send supplied keywords, links, or IDs to the third-party GUAIKEI service; account search and lead identification are available.

Mitigation: Review query inputs before use, avoid sending sensitive links or identifiers, and use account discovery and lead identification only when appropriate for the intended analysis.

Risk: Security inspection was partial: 31 of 53 components were fully inspected and 22 were partially inspected.

Mitigation: Review the requested behavior before installation and enable only the capabilities needed for the task.

## Reference(s):

- [Demand mining guidance](references/demand-mining.md)
- [Customer acquisition guidance](references/customer-acquisition.md)
- [Output contract](references/contract.md)
- [GUAIKEI service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Shell commands, Guidance]

**Output Format:** [Structured JSON results with concise analysis or guidance when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can include post and creator details, engagement counts, timestamps, links, and comment text where available.]

## Skill Version(s):

1.5.0 (source: server-resolved release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
