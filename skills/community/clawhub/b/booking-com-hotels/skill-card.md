## Description:

Search Booking.com hotels by location, dates and occupancy in one unified schema, with cross-OTA price comparison. Use for hotel discovery on Booking.com. Powered by StayingAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stayingapi](https://clawhub.ai/user/stayingapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Booking.com hotel stays by destination, dates, occupancy, and filters through StayingAPI, then compare rates across supported travel platforms when coverage is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a StayingAPI key and its setup guide asks the agent to persist it in an unspecified place across sessions.

Mitigation: Use a sandbox stay_test_ key for evaluation and store live keys only in an agent or runtime secret store, not in project files or shell profiles.

Risk: Live hotel and price data depends on StayingAPI and upstream platform coverage, so results or cross-OTA comparisons can be partial or single-offer.

Mitigation: Check response metadata, warnings, offers.length, and job status before presenting availability or multi-platform comparisons as complete.

## Reference(s):

- [StayingAPI homepage](https://stayingapi.com)
- [StayingAPI docs](https://stayingapi.com/docs)
- [StayingAPI OpenAPI contract](https://api.stayingapi.com/openapi.json)
- [StayingAPI MCP server](https://mcp.stayingapi.com/mcp)
- [StayingAPI pricing](https://stayingapi.com/pricing)
- [Authentication setup](references/auth-setup.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and API request details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include StayingAPI REST calls, polling guidance, hotel search results, and price-comparison guidance.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
