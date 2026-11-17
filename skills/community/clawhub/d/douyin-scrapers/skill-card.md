## Description:

Searches public Douyin videos and posts, retrieves trending lists, creator works, item details, and comments, and returns structured engagement data for content analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Content analysts, creators, and marketing teams use the skill to find public Douyin content, monitor creator posts and trends, and review engagement or comments for planning and internal analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and supplied Douyin links are sent to the third-party Guaikei API.

Mitigation: Use only public data and authorized queries, and review the service terms and privacy practices before sending queries.

Risk: The security review was benign but had medium confidence because analysis coverage was incomplete and the tool-misuse analyzer was degraded.

Mitigation: Review the available security results and coverage limits before deployment, and keep the skill's read-only, public-data scope.

## Reference(s):

- [Guaikei service and help](https://www.guaikei.com)
- [Command options](references/options.md)
- [Comment analysis guidance](references/demand-mining.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Shell commands, Guidance]

**Output Format:** [Structured JSON results with concise content and engagement analysis; shell commands for requesting data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result fields vary by command. Query limits depend on the token plan, and returned media links may expire.]

## Skill Version(s):

1.4.2 (source: changelog, released 2026-11-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
