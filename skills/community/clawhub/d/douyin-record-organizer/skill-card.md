## Description:

Retrieves public Douyin videos, creator posts, comments, trends, and engagement metrics as structured data for content research and analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Content creators, analysts, and marketing teams use this skill to search public Douyin content, monitor trends and creator posts, inspect engagement and comments, and organize the results for content and audience analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and Douyin links are sent to the third-party GUAIKEI API, and use requires an API token.

Mitigation: Use only public content and non-sensitive queries; confirm the data-sharing scope and keep GUAIKEI_API_TOKEN private.

Risk: ClawScan reports a benign result with medium confidence, but its code analysis is incomplete and its tool-misuse analysis was degraded.

Mitigation: Review the skill and use it only if its stated purpose and remaining analysis uncertainty are acceptable.

## Reference(s):

- [Demand mining guide](references/demand-mining.md)
- [Command options](references/options.md)
- [Changelog](references/changelog.md)
- [GUAIKEI website and token support](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON data, Analysis, Guidance]

**Output Format:** [Structured JSON records and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public content; results may include engagement metrics and links. Video and share links may expire.]

## Skill Version(s):

1.4.2 (source: changelog, released 2026-11-04; package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
