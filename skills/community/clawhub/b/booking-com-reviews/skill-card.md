## Description:

Read normalized Booking.com reviews for a listing, with native rating scales preserved. Use when a user wants ratings or guest feedback for a listing on Booking.com. Powered by StayingAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stayingapi](https://clawhub.ai/user/stayingapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve normalized Booking.com guest reviews and rating details for a known listing while preserving the platform's native rating scale.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live API keys can expose paid account access if pasted into prompts or committed to source control.

Mitigation: Store STAYINGAPI_KEY in a protected environment file or secret manager, and use a sandbox key for evaluation.

Risk: The documentation mentions broader StayingAPI platform and endpoint capabilities than Booking.com reviews alone.

Mitigation: Use this skill for Booking.com review requests and verify platform support before describing other endpoint capabilities.

Risk: Sandbox fixtures may not mirror the requested property or travel details.

Mitigation: Use sandbox responses only for parsing and integration checks, then switch to a live key for real review data.

## Reference(s):

- [StayingAPI authentication setup](references/auth-setup.md)
- [StayingAPI homepage](https://stayingapi.com)
- [StayingAPI documentation](https://stayingapi.com/docs)
- [StayingAPI OpenAPI contract](https://api.stayingapi.com/openapi.json)
- [StayingAPI MCP server](https://mcp.stayingapi.com/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with API request details and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires STAYINGAPI_KEY and internet access to api.stayingapi.com; preserves native review rating scales and uses pagination, async job, and platform support details from the skill documentation.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
