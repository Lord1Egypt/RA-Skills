## Description:

Discover winning game and app ad creatives from Denote's weekly Trending, Rising, and New Ads charts. Use for creative research, weekly ad inspiration, free account setup, or a closer look at a ranked ad.

This skill is ready for commercial/non-commercial use.

## Publisher:

[denote-developer](https://clawhub.ai/user/denote-developer)

### License/Terms of Use:

MIT-0

## Use Case:

Advertisers, user acquisition teams, and creative researchers can compare weekly game and utility app ad rankings and inspect individual creatives. The rankings offer ideas for planning campaign tests; chart positions do not establish sales, return on ad spend, or spend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes authenticated network requests and does not declare its tool scope.

Mitigation: Review its network access before installation, and store a Denote key with only the top_ads:read scope in the agent host's secret settings.

## Reference(s):

- [Denote Top Ads](https://denote.net/top-ads)
- [Server-resolved source repository](https://github.com/denote-developer/denote-top-ads)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML report]

**Output Format:** [Markdown tables and a localized HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports use weekly rankings; individual creative details depend on account permissions and plan.]

## Skill Version(s):

0.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
