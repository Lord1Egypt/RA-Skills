## Description:

Retrieves Douyin follower-growth ranking data by day, week, or month and category, then summarizes account rankings, follower counts, growth rates, fan increases, and operational insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[if530770](https://clawhub.ai/user/if530770)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, brand marketers, MCN operators, and advertising teams use this skill to monitor Douyin account follower-growth rankings across vertical categories and time windows. It supports competitive tracking, content planning, account selection, and trend analysis using Redfox Hub ranking data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flagged instruction-priority override language in the artifact.

Mitigation: Review and remove language that tells an agent to override higher-priority platform, system, or user policies before deployment.

Risk: The fetch script may read shell startup files to locate REDFOX_API_KEY.

Mitigation: Provide the API key only through an explicit environment variable or approved secret manager, and review local credential handling before installation.

Risk: Generated account links and API-returned fields are rendered into Markdown.

Mitigation: Validate returned links and display fields before rendering or clicking them.

Risk: The artifact claims subscription behavior that the evidence does not show as a real user-controlled notification system.

Mitigation: Treat subscription prompts as unsupported until a reviewed notification implementation and user controls exist.

## Reference(s):

- [Core workflow](artifact/references/core_workflow.md)
- [Douyin ranking API reference](artifact/references/dy-rank-api.md)
- [Redfox Hub](https://redfox.hk/)
- [Redfox Douyin follower-growth ranking API endpoint](https://redfox.hk/story/api/dyData/getDyRiseFansRank)
- [ClawHub skill page](https://clawhub.ai/if530770/skills/douyin-rise-ranking)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Guidance]

**Output Format:** [Markdown ranking tables and analysis, with JSON available from the fetch script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY and may cache the latest successful lookup locally.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
