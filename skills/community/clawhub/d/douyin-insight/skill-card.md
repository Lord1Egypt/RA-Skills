## Description:

Analyzes public Douyin content for competitor insights through keyword search, trending lists, creator and post details, and comment data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, creators, and analysts use the skill to research public Douyin trends, compare creator activity, and organize content and audience insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and Douyin targets are sent to a third-party API, whose behavior and data-retention practices were not verified.

Mitigation: Use the service only when third-party processing is acceptable, and avoid sending sensitive search terms or targets.

Risk: The API token, usage charges, and locally saved query/result logs need care.

Mitigation: Protect the API token, check usage charges, and manage saved query/result logs.

## Reference(s):

- [ClawHub release](https://clawhub.ai/why20261/skills/douyin-insight)
- [API access and support](https://www.guaikei.com)
- [CLI options](artifact/references/options.md)
- [Comment demand analysis guide](artifact/references/demand-mining.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search, trends, creator posts, post details, and comments; query and result logs are saved locally.]

## Skill Version(s):

1.4.2 (source: server-resolved release; artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
