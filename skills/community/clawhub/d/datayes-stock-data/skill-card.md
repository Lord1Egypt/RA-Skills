## Description:

Queries Datayes for A-share and Hong Kong stock prices, intraday and K-line data, financials, valuation metrics, fund flows, shareholder holdings, dividends, and company profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shermanxli](https://clawhub.ai/user/shermanxli)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer stock market and listed-company questions with Datayes data, including real-time prices, fundamentals, valuations, rankings, fund flows, technical indicators, and company profiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Datayes API token could be forwarded outside the intended host allowlist during redirects.

Mitigation: Use a minimal-scope, revocable token and reject cross-origin redirects or strip Authorization on redirected requests before deployment.

## Reference(s):

- [Datayes API Catalog](references/api-catalog.md)
- [ClawHub skill page](https://clawhub.ai/shermanxli/skills/datayes-stock-data)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and DATAYES_TOKEN; API responses should be summarized with time range, units, and data basis.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
