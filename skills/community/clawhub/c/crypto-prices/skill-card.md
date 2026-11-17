## Description:

Helps agents fetch and format live cryptocurrency and commodity price data from configured market data providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryandeangraves](https://clawhub.ai/user/ryandeangraves)

### License/Terms of Use:


## Use Case:

Agents use this skill when a user asks for current cryptocurrency or commodity prices, including batch lookups and concise market-price summaries. It is intended for price lookup support, not financial advice or trade execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Price lookup requests are sent to external market data providers, which may expose queried assets and depend on provider availability, rate limits, and data quality.

Mitigation: Use the skill only for intended market-price lookups, avoid including sensitive trading context in requests, and report prices as unavailable when providers fail.

Risk: The skill depends on an existing local ~/clawd/crypto_prices.py module that was not included in the reviewed skill package.

Mitigation: Confirm the local module is present, trusted, and reviewed before enabling the skill or running its commands.

Risk: Cached or provider-returned market data can become stale or incomplete.

Mitigation: Prefer outputs that include source context, do not guess missing prices, and refresh results when accuracy is material.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with bash command examples and formatted price text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a short cache window and provider fallback behavior when the local price module is available.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
