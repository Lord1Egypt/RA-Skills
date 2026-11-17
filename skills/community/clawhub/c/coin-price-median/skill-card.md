## Description:

AirnodeHub coin price skill for crypto price requests: fetch all available specialist source prices, report each value, median, and deviation from median.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metobom](https://clawhub.ai/user/metobom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to answer crypto asset or pair price requests by collecting specialist AirnodeHub source prices, computing a median, and showing each source's deviation from that median.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes network requests to AirnodeHub provider listings, and some calls may be paid, metered, credentialed, or quota-consuming.

Mitigation: Review provider documentation before use, approve any paid or uncertain call explicitly, and skip unapproved sources from the median.

Risk: Aggregated crypto price output could be misread as financial advice.

Mitigation: Present the result as price aggregation with source attribution and avoid personalized buy or sell recommendations.

## Reference(s):

- [AirnodeHub catalogue](https://airnode-v2-hub.api3.org/llms.txt)
- [ClawHub skill page](https://clawhub.ai/metobom/skills/coin-price-median)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown table with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source attribution, timestamps when returned, verification status, median price, and per-source deviation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
