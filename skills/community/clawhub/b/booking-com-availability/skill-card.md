## Description:

Check day-by-day Booking.com availability (the booking calendar) for a known listing over a date window.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stayingapi](https://clawhub.ai/user/stayingapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check whether a known Booking.com listing is available over requested dates through StayingAPI. It is useful when an agent needs day-by-day availability, setup guidance for STAYINGAPI_KEY, or handling guidance for async availability jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Listing identifiers, listing URLs, requested date windows, and the StayingAPI key are sent to StayingAPI.

Mitigation: Use a sandbox key for evaluation and store live keys in a scoped secret manager or agent-managed environment rather than broad shell profiles where possible.

Risk: Live availability checks can return async, partial, empty, failed, or rate-limited results.

Mitigation: Respect Retry-After, back off between polling attempts, cap retries, and inspect job status plus warnings before reporting availability to the user.

## Reference(s):

- [Authentication setup](references/auth-setup.md)
- [StayingAPI homepage](https://stayingapi.com)
- [StayingAPI documentation](https://stayingapi.com/docs)
- [StayingAPI OpenAPI contract](https://api.stayingapi.com/openapi.json)
- [StayingAPI MCP server](https://mcp.stayingapi.com/mcp)
- [StayingAPI pricing](https://stayingapi.com/pricing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with availability summaries, inline shell commands, and API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include per-day availability status, minimum-night constraints, async polling guidance, and authentication setup using STAYINGAPI_KEY.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
