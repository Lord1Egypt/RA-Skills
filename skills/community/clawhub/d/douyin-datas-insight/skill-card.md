## Description:

Retrieves public Douyin search, creator, video, comment, and trending data as structured JSON for content research and analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Content teams and analysts use this skill to search public Douyin videos, inspect creator posts and individual videos, collect comments or trending topics, and prepare structured data for topic research, competitor tracking, and sentiment analysis. Use requires a token and sends requested keywords or links to a third-party data API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan rates the skill suspicious because broad activation phrases could route unrelated requests to Douyin searches, and parts of the code were only partially inspected.

Mitigation: Limit activation to explicit Douyin requests and review the partially inspected code before installation.

Risk: Requested keywords or links are sent to a third-party API.

Mitigation: Check that sharing those query details with the API fits the user's intended use.

## Reference(s):

- [Parameter reference](references/options.md)
- [Comment demand-mining guide](references/demand-mining.md)
- [Changelog](references/changelog.md)
- [Guaikei service and token help](https://www.guaikei.com)
- [ClawHub release page](https://clawhub.ai/why20261/skills/douyin-datas-insight)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON with concise analysis or reports when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Contains public search, creator, video, comment, and trending data; availability and fields depend on the service.]

## Skill Version(s):

1.4.2 (source: SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
