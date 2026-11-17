## Description:

Search live Booking.com stays by location, dates, and occupancy through StayingAPI, returning results in the same unified schema used across supported booking platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stayingapi](https://clawhub.ai/user/stayingapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Booking.com accommodations by location, dates, occupancy, and filters, then handle the resulting StayingAPI responses in a normalized property schema.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses the external StayingAPI service and requires a StayingAPI credential.

Mitigation: Use a stay_test_ sandbox key for evaluation, keep live keys in an environment or secret store, and avoid pasting credentials into agent prompts.

Risk: Searches can fan out across multiple booking platforms if platform scope is not constrained.

Mitigation: Pass platforms=booking when the user only wants Booking.com results or when billing scope should be limited to Booking.com searches.

Risk: Live results can be asynchronous, paginated, empty, rate-limited, or partially unavailable depending on upstream platform coverage.

Mitigation: Honor Retry-After headers, cap polling attempts, read job status and meta.pagination as authoritative, and surface warnings or failed job states to the user.

## Reference(s):

- [StayingAPI auth setup](references/auth-setup.md)
- [StayingAPI](https://stayingapi.com)
- [StayingAPI docs](https://stayingapi.com/docs)
- [StayingAPI OpenAPI contract](https://api.stayingapi.com/openapi.json)
- [ClawHub skill page](https://clawhub.ai/stayingapi/skills/booking-com-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with REST and MCP request details, parameter descriptions, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include REST API calls using STAYINGAPI_KEY and Booking.com-filtered search parameters.]

## Skill Version(s):

1.1.0 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
