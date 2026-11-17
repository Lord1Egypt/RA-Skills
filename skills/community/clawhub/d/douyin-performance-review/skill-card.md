## Description:

Collects public Douyin search, trending, post, creator, and comment data as structured JSON to support performance reviews and testable content strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Social media operators, content analysts, and marketing teams use this skill to review public Douyin posts and engagement, monitor creators and trends, analyze comments, and shape testable content strategies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security scan coverage is incomplete: 18 of 42 components were only partially inspected.

Mitigation: Review the skill before installation and use it only in an environment where its required access is acceptable.

Risk: The skill sends the supplied Douyin keyword or link and an API token to the GUAIKEI service to retrieve data.

Mitigation: Use only public, non-sensitive queries and keep GUAIKEI_API_TOKEN private in a trusted secret store.

Risk: Retrieved data may include public user comments and engagement information that should not be redistributed without care.

Mitigation: Keep analysis within personal or team use, consistent with the skill documentation.

## Reference(s):

- [GUAIKEI service and API access](https://www.guaikei.com)
- [ClawHub release](https://clawhub.ai/why20261/skills/douyin-performance-review)
- [Demand mining guide](references/demand-mining.md)
- [Command options](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Markdown]

**Output Format:** [Structured JSON data with concise content performance analysis and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public Douyin data. Query limits depend on the API token plan; media and share links may expire.]

## Skill Version(s):

1.4.2 (source: frontmatter, package.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
