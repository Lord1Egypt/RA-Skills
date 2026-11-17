## Description:

Get a real Airbnb price quote for a listing and dates, then compare that property against the offers StayingAPI can resolve for it to find the cheapest rate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stayingapi](https://clawhub.ai/user/stayingapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to quote a specific lodging listing for requested dates and occupancy, then compare available offers for the same property when StayingAPI can resolve them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a StayingAPI key for API requests, and live keys could be exposed if pasted into chats or logs.

Mitigation: Store STAYINGAPI_KEY in an agent or OS secret store when available, use sandbox keys for testing, and rotate or revoke any key suspected of exposure.

Risk: The skill makes network requests to StayingAPI and depends on upstream coverage for exact property matching and cross-OTA offers.

Mitigation: Use live responses for real identity and price claims, read offers.length before presenting a result as multi-platform comparison, and disclose when only an aggregated-lowest offer is available.

Risk: Sandbox responses are fixture data and may not match requested listing IDs, dates, or occupancy.

Mitigation: Use sandbox keys only for evaluation and parsing checks; switch to a live key before presenting real prices.

Risk: Async polling can encounter failed jobs or rate limits if polled too aggressively.

Mitigation: Honor Retry-After headers, back off between polling attempts, cap retries, and inspect terminal job status instead of assuming HTTP 200 means success.

## Reference(s):

- [Airbnb prices & cross-OTA comparison on ClawHub](https://clawhub.ai/stayingapi/skills/airbnb-prices)
- [StayingAPI](https://stayingapi.com)
- [StayingAPI docs](https://stayingapi.com/docs)
- [StayingAPI OpenAPI contract](https://api.stayingapi.com/openapi.json)
- [StayingAPI auth setup](references/auth-setup.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with inline API request guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe REST or MCP calls that require internet access and a STAYINGAPI_KEY.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
