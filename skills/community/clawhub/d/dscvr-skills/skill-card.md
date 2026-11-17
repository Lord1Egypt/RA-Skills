## Description:

Queries DSCVR crypto intelligence APIs for market news, event tracking, smart money analysis, prediction market data, AI-powered event discovery, market orderbooks, and social graph data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dscvr-release](https://clawhub.ai/user/dscvr-release)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve and summarize DSCVR market intelligence, including crypto news events, smart money trader activity, prediction market data, AI-discovered events, orderbook depth, and DSCVR social graph information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Endpoint configuration could direct authenticated requests to a service other than the official DSCVR API.

Mitigation: Keep DSCVR_API_BASE_URL unset or set it only to the official HTTPS DSCVR service.

Risk: GraphQL queries, wallet lookups, usernames, and market research requests are sent to DSCVR's external API.

Mitigation: Avoid submitting sensitive internal research unless disclosure to DSCVR is acceptable.

Risk: The skill requires DSCVR API credentials for authenticated network requests.

Mitigation: Store DSCVR_API_KEY and DSCVR_SECRET_KEY as secrets and avoid exposing them in prompts, logs, or shared transcripts.

Risk: Authentication failures, clock skew, or high request volume can trigger temporary bans or rate limiting.

Mitigation: Keep system time synchronized, verify credentials before repeated retries, and throttle requests when HTTP 429 or 403 responses occur.

## Reference(s):

- [DSCVR Intelligence API Reference](references/api-reference.md)
- [DSCVR API Authentication Reference](references/auth-reference.md)
- [DSCVR API Service](https://dscvr.one)
- [DSCVR Subscription](https://dscvr.one/subscription)
- [uv Installation Guide](https://docs.astral.sh/uv/getting-started/installation/)
- [PEP 723 Inline Script Metadata](https://packaging.python.org/en/latest/specifications/inline-script-metadata/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown summaries with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DSCVR API credentials and network access; results depend on DSCVR API availability, rate limits, and the requested market or social data.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
