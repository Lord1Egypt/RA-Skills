## Description:

futurespro-panda queries futures fees, margins, special-variety account conditions, trading announcements, trading calendars, and futures company lists through HTTP API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mabtush13](https://clawhub.ai/user/mabtush13)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve futures-market reference data, including product fees, margin information, special-product eligibility conditions, recent trading announcements, calendar events, and futures company lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API calls can be redirected to arbitrary addresses.

Mitigation: Use only a fixed, trusted HTTPS API origin and validate the endpoint before execution.

Risk: The documented curl examples use insecure TLS options.

Mitigation: Remove insecure TLS flags and require certificate validation for financial-data requests.

Risk: Query terms are sent to an external API.

Mitigation: Disclose the external API use and avoid private endpoints, account-specific trading details, proprietary strategies, or sensitive internal network addresses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mabtush13/skills/futurespro-panda)
- [Publisher profile](https://clawhub.ai/user/mabtush13)
- [FuturesPro Panda API base URL](https://124.221.52.208)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance]

**Output Format:** [Markdown with inline shell commands and summarized API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may return financial reference data from an external HTTP API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
