## Description:

A Douyin assistant that retrieves public video, creator, comment, and trending data for sentiment, audience, intent, and content analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Content creators, social media operators, brands, and e-commerce teams use the skill to find public Douyin videos and creator posts, review comments and trends, and prepare sentiment, audience, intent, and content insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided keywords and links are sent to the third-party GuaiKei API; this may expose sensitive query or content context.

Mitigation: Avoid sending confidential or personal information, and use the skill only with data approved for external processing.

Risk: The benign security verdict is based on partial analysis and leaves some uncertainty.

Mitigation: Review the skill’s instructions and behavior before installation, and follow your organization’s review process for third-party skills.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/why20261/skills/douyin-comments-sentiment)
- [GuaiKei API service and token access](https://www.guaikei.com)
- [Demand mining guide](artifact/references/demand-mining.md)
- [Command options](artifact/references/options.md)
- [Release changelog](artifact/references/changelog.md)
- [Output envelope schema](artifact/assets/output_envelope.schema.json)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON records with human-readable analysis and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on public Douyin data and the configured service plan; returned data may be empty or unavailable.]

## Skill Version(s):

1.4.2 (source: server-resolved release, package.json, changelog released 2026-11-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
