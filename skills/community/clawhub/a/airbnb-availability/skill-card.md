## Description:

Check day-by-day Airbnb availability for a known listing over a date window, powered by StayingAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stayingapi](https://clawhub.ai/user/stayingapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to check whether a known Airbnb listing is available across specific dates. It is suited for calendar availability checks, not listing discovery or price lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends listing and date-window queries to StayingAPI and requires a secret API key.

Mitigation: Use a secure runtime secret store for STAYINGAPI_KEY, avoid committing the key, and use a stay_test_ sandbox key for evaluation when possible.

Risk: Live API calls depend on network access and may return asynchronous jobs, empty results, or failed jobs.

Mitigation: Poll according to the documented Retry-After and backoff guidance, cap attempts, and treat nested job status and warnings as authoritative.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stayingapi/skills/airbnb-availability)
- [StayingAPI homepage](https://stayingapi.com)
- [StayingAPI docs](https://stayingapi.com/docs)
- [StayingAPI OpenAPI contract](https://api.stayingapi.com/openapi.json)
- [Authentication setup](references/auth-setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with API request examples and availability result interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires STAYINGAPI_KEY and network access to StayingAPI; live availability calls may return asynchronous jobs that need polling.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
