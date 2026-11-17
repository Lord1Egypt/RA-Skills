## Description:

Searches public Douyin videos, creator profiles, comments, and trending topics, returning structured data for content and market research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

External users and content or market researchers can search public Douyin content, inspect creator activity, review comments and trends, and use the returned data to inform content planning, competitor analysis, and market research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and Douyin links are sent to the third-party provider API.

Mitigation: Send only queries and public links that are appropriate for third-party processing; avoid sensitive search terms or URLs.

Risk: The security assessment is benign with medium confidence because inspection was partial (24 of 42 components fully inspected).

Mitigation: Treat the verdict as limited evidence and review the remaining components before deployment.

Risk: Supported commands save retrieved data and query details in local logs/ files.

Mitigation: Limit access to those files and remove them when they are no longer needed.

## Reference(s):

- [Search and command options](references/options.md)
- [Comment demand-mining guide](references/demand-mining.md)
- [Output envelope schema](assets/output_envelope.schema.json)
- [Provider website](https://www.guaikei.com)
- [ClawHub listing](https://clawhub.ai/why20261/skills/douyin-research)

## Skill Output:

**Output Type(s):** [JSON, Text analysis, Guidance]

**Output Format:** [Structured JSON results, with concise text analysis when interpreting results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14+ and GUAIKEI_API_TOKEN. Queries use public Douyin data through the provider API; supported command results are saved under logs/.]

## Skill Version(s):

1.4.2 (source: SKILL.md frontmatter, package.json, changelog dated 2026-11-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
