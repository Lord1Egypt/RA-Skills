## Description:

Compare public event forecasts across Crawlora's Polymarket, Kalshi, and Metaculus tools while preserving question rules, outcomes, scales, timestamps, and market context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and developers use this skill to compare matched public event forecasts and explain dated divergences without treating unlike questions or market prices as equivalent probabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Crawlora API key and forecast queries are sent to Crawlora, and requests can consume credits.

Mitigation: Treat the key as a credential and limit queries and pages to the intended credit budget.

Risk: Differences in resolution rules, outcome labels, timing, and liquidity can make forecast comparisons misleading.

Mitigation: Check the proposition match and source timestamps; report incomparable values separately and qualify any divergence.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/crawlora-org/skills/forecast-consensus-comparison)
- [Endpoint reference](reference/endpoints.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown comparison tables and dated narrative]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Source-attributed proposition matches, forecast snapshots or history, divergence calculations, and uncertainty.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
