## Description:

Finds, screens, and reviews Douyin creators for collaboration using public video, creator, engagement, trend, and comment data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Brand marketers and content teams use this skill to discover and assess public Douyin creators for potential partnerships. It helps compare content and engagement signals, audience fit, and commercial costs, then prepare a data-backed candidate shortlist.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment is benign but has medium confidence and only partially inspected 18 of 42 components, leaving uncertainty about behavior in those files.

Mitigation: Review the executable files and security assessment before relying on the skill in a sensitive environment.

Risk: Queries and Douyin links are sent to the GUAIKEI third-party API, and returned data is intended for personal or team analysis rather than unauthorized redistribution.

Mitigation: Avoid sending sensitive information, confirm the query and data use are authorized, and keep results within the permitted internal use scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/why20261/skills/douyin-creator-screening)
- [Publisher profile](https://clawhub.ai/user/why20261)
- [GUAIKEI service and token access](https://www.guaikei.com)
- [Skill usage and safety guidance](SKILL.md)
- [Command options](references/options.md)
- [Comment analysis guidance](references/demand-mining.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Markdown]

**Output Format:** [Structured JSON data with concise findings, candidate summaries, or Markdown tables and reports when requested.]

**Output Parameters:** [Variable; searches and retrievals accept filters and result limits.]

**Other Properties Related to Output:** [Uses public Douyin data and requires GUAIKEI_API_TOKEN. Available result limits depend on the token plan.]

## Skill Version(s):

1.4.2 (source: SKILL.md frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
