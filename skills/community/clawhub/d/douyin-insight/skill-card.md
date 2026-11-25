## Description:

This skill retrieves public Douyin videos, creator profiles, post details, comments, and trending topics for competitor and content analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Douyin marketers, creators, and analysts use the skill to research competitor content, discover relevant creators, track trending topics, and inspect engagement and comments. Its results support content planning, competitor monitoring, and audience insight work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted search terms, links, or IDs are sent to a third-party API.

Mitigation: Tell the user before querying and avoid sending sensitive or private identifiers.

Risk: The release includes keyword-based account search beyond its declared capabilities.

Mitigation: Make the account-search capability clear and confirm before using it when the user has not requested account discovery.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/why20261/skills/douyin-insight)
- [GuaiKei API access and support](https://www.guaikei.com)
- [Output contract](artifact/references/contract.md)
- [Demand mining guidance](artifact/references/demand-mining.md)

## Skill Output:

**Output Type(s):** [JSON data, Analysis, Guidance]

**Output Format:** [Structured JSON results with concise written analysis or recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can include public post, creator, engagement, trend, and comment information; users should request an appropriate result count.]

## Skill Version(s):

1.5.0 (source: SKILL.md frontmatter, package.json, changelog, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
