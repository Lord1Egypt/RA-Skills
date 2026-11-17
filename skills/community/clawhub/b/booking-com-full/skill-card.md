## Description:

Complete Booking.com toolkit — search, availability, listing detail, price, cross-OTA price comparison and reviews, all in one unified schema.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stayingapi](https://clawhub.ai/user/stayingapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when an agent needs to query StayingAPI for Booking.com lodging search, availability, listing details, prices, cross-OTA price comparison, and reviews through a unified schema.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends travel search requests and related lodging details to StayingAPI using a user-provided API key.

Mitigation: Avoid sending sensitive trip details unless the user is comfortable sharing them with StayingAPI.

Risk: Live API calls may spend applicable StayingAPI credits.

Mitigation: Use a stay_test_ sandbox key for evaluation and switch to a live key only when real data is needed.

Risk: A live API key grants access to StayingAPI requests.

Mitigation: Store live keys in a secure secret store when possible and avoid pasting them into shared logs or prompts.

## Reference(s):

- [Authentication setup](references/auth-setup.md)
- [StayingAPI homepage](https://stayingapi.com)
- [StayingAPI documentation](https://stayingapi.com/docs)
- [StayingAPI OpenAPI contract](https://api.stayingapi.com/openapi.json)
- [StayingAPI MCP server](https://mcp.stayingapi.com/mcp)
- [ClawHub skill page](https://clawhub.ai/stayingapi/skills/booking-com-full)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with endpoint guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires STAYINGAPI_KEY and internet access to api.stayingapi.com.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
