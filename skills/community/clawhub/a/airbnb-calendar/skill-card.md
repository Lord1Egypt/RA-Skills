## Description:

Read an Airbnb listing calendar -- day-by-day availability over a date window for known listing IDs or listing URLs, powered by StayingAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stayingapi](https://clawhub.ai/user/stayingapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check whether known Airbnb listings are available for specific date windows and to retrieve day-level booking constraints such as minimum nights, check-in, check-out, and booking availability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a StayingAPI key, and poor secret handling could expose account credentials.

Mitigation: Store STAYINGAPI_KEY in a runtime secret store, OS keychain, or tightly permissioned secrets file; avoid committing it to dotfiles or logs, and use a sandbox key for testing when possible.

Risk: Availability calls depend on live upstream data and may return asynchronous jobs, empty results, partial results, or failed jobs.

Mitigation: Poll according to Retry-After guidance, cap retry attempts, inspect job status and warnings, and avoid treating empty or partial results as confirmed availability.

Risk: Overly frequent polling can trigger rate limiting.

Mitigation: Back off between polling attempts and avoid tight loops when checking job status.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/stayingapi/skills/airbnb-calendar)
- [StayingAPI homepage](https://stayingapi.com)
- [StayingAPI docs](https://stayingapi.com/docs)
- [StayingAPI OpenAPI contract](https://api.stayingapi.com/openapi.json)
- [StayingAPI MCP server](https://mcp.stayingapi.com/mcp)
- [Auth setup](references/auth-setup.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with API request details and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires STAYINGAPI_KEY and internet access to api.stayingapi.com for live API calls.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
