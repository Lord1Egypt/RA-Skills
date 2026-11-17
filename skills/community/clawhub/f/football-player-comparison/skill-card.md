## Description:

Compares football players using Crawlora FotMob profiles, season statistics, and bounded match samples while preserving role, playing time, competition, and source context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and scouts use this skill to compare football players across matched roles and periods, prepare statistical scouting briefs, and explain recent form with source and sample limitations visible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Player lookup and statistics queries are sent to Crawlora using an API key.

Mitigation: Use only if comfortable sharing those queries, keep CRAWLORA_API_KEY private, and prefer the listed MCP tools when available.

Risk: Authenticated queries can consume API credits.

Mitigation: Set a bounded match and page scope, and review API credit usage.

Risk: Unmatched competitions, roles, or playing time can make statistical comparisons misleading.

Mitigation: Compare matched scopes, show minutes and denominators, and disclose missing data and small samples.

## Reference(s):

- [Endpoint reference](reference/endpoints.md)
- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/football-player-comparison)
- [ClawHub publisher profile](https://clawhub.ai/user/crawlora-org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Markdown comparison with an identity and scope ledger, metric table, formulas, match evidence, and uncertainties]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports minutes and denominators; rankings require user criteria and disclosed weights.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
