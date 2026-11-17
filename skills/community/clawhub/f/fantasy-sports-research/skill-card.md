## Description:

Compare public daily-fantasy contest formats, rules, slates, and source-published player projections from DraftKings and FanDuel. Use for fantasy-sports research, not lineup or wager recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

External fantasy-sports researchers use this skill to compare public DraftKings and FanDuel contest formats, rules, slates, and provider projection fields without receiving lineup or wager recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crawlora receives the submitted query parameters and authentication key, and requests consume API credits.

Mitigation: Keep the API key private, send only the query parameters needed for the research, and account for API credit use.

Risk: Provider projections can be mistaken for actual outcomes or independent forecasts.

Mitigation: Label projections as provider estimates, preserve their source slate and scoring context, and do not present them as guarantees, expected returns, or winning probabilities.

## Reference(s):

- [Fantasy sports research endpoint reference](artifact/reference/endpoints.md)
- [Crawlora API v1](https://api.crawlora.net/api/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise source-attributed Markdown table or overview]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source date, sport, contest type, selection scope, and unavailable fields; separates official rules from provider estimates.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
