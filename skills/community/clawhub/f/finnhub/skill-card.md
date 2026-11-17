## Description:

Access Finnhub API for real-time stock quotes, company news, market data, financial statements, and trading signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthewxfz3](https://clawhub.ai/user/matthewxfz3)

### License/Terms of Use:


## Use Case:

Developers and market-data users use this skill to configure Finnhub API access and request quotes, company news, financial statements, earnings data, market indicators, SEC filing search, and trading signal data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Finnhub API keys can be exposed when tokenized request URLs are copied into logs, telemetry, support tickets, or command output.

Mitigation: Use a restricted Finnhub key where possible, store it with owner-only permissions, avoid pasting expanded URLs, and rotate the key if exposure is suspected.

Risk: Some Finnhub endpoints require paid tiers or are subject to rate limits, which can lead to failed or incomplete requests.

Mitigation: Confirm the account tier and endpoint limits before relying on generated requests, and handle rate-limit or subscription errors explicitly.

## Reference(s):

- [Finnhub](https://finnhub.io)
- [Finnhub API base URL](https://finnhub.io/api/v1)
- [ClawHub skill page](https://clawhub.ai/matthewxfz3/skills/finnhub)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FINNHUB_API_KEY for live Finnhub requests.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
