## Description:

Researches football fixtures, match reports, player form, transfers, standings, and broadcast listings through Crawlora's FotMob tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Football researchers, analysts, and fans use this skill to prepare source-attributed match briefs, compare teams or players, review league standings and transfers, and find broadcast listings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Football lookup queries and the user's API key are sent to Crawlora, and requests may consume credits.

Mitigation: Keep CRAWLORA_API_KEY secret and limit requests to the intended scope and credit budget.

Risk: Some news and media feeds use English or an English-US variant, and availability may differ by market.

Mitigation: Check the feed's language and market before relying on news or media availability.

Risk: Unconfirmed transfer rumours, provider estimates, and incomplete match data may be mistaken for established facts.

Mitigation: Label rumours and estimates, cite sources and observation times, and mark unavailable statistics as unknown.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/fotmob-research)
- [FotMob endpoint reference](reference/endpoints.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown brief and evidence table with source links and timestamps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Distinguishes unconfirmed transfers and missing data from confirmed results.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
