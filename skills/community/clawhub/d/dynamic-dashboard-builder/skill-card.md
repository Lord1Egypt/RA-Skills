## Description:

Helps an agent build dynamic HTML dashboards from existing database tables with periodic data refresh after confirming the endpoint, polling interval, schema, and data exposure constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmuhammadagus-byte](https://clawhub.ai/user/pmuhammadagus-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to create HTML dashboards backed by approved existing database tables and periodically refreshed API data. It is intended for dashboard setup where endpoint trust, polling rate, schema changes, and sensitive data exposure must be confirmed before implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted or hardcoded API endpoints can expose dashboard data or create brittle integrations.

Mitigation: Use only trusted, explicitly approved endpoints and keep endpoint values in environment variables or configuration.

Risk: Polling too frequently can violate rate limits or overload an API.

Mitigation: Confirm the polling interval with the user, default to 300 seconds, and apply backoff behavior for rate-limit responses.

Risk: Dashboards can expose sensitive or personally identifiable data.

Mitigation: Confirm that no sensitive or PII data will be exposed, sanitize data before rendering, and avoid logging secrets or sensitive records.

Risk: Unapproved schema creation or alteration can damage existing data structures.

Mitigation: Require user review and explicit approval before any CREATE or ALTER operation and stop on invalid schemas.

Risk: API, authentication, or network failures can leave users with blank or misleading dashboards.

Mitigation: Render graceful error states, use cached data when appropriate, alert immediately on authentication failures, and limit retries for network timeouts.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with JavaScript and HTML code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated guidance should keep endpoints configurable, require user-approved polling and schema changes, sanitize rendered data, and avoid exposing sensitive or PII data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
