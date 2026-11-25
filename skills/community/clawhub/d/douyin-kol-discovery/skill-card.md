## Description:

Retrieve Douyin creators using keyword search, creator and post data, engagement metrics, comments, and trending topics to help users evaluate creators and content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Content strategists, marketing teams, and analysts can discover Douyin creators, review public creator and post metrics, track trends, and analyze public comments for content, competitor, and audience research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks the skill suspicious because ambiguous requests may trigger Douyin searches, and 22 of 53 components were only partially inspected.

Mitigation: Review the requested query and linked profile or post before running it; use explicit keywords and URLs, and inspect the artifact before installation.

Risk: Search keywords and Douyin links are sent to the third-party service at guaikei.com.

Mitigation: Avoid sending sensitive or identifying information; run searches only when the user intends to share the query with that service.

## Reference(s):

- [Routing guide](references/routing.md)
- [Command options](references/options.md)
- [Output contract](references/contract.md)
- [Service website and token access](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON results with creator, post, engagement, comment, and trend data, followed by concise analysis when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results use a consistent JSON envelope; most query results are also saved in the skill's logs directory.]

## Skill Version(s):

1.5.0 (source: evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
