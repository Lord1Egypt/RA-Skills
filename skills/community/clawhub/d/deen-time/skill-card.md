## Description:

Get daily Islamic prayer (Salah) times, Iftar, and Suhoor schedules for any location worldwide. Supports 15+ calculation methods, Hijri dates, and Ramadan calendars.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fermions75](https://clawhub.ai/user/fermions75)

### License/Terms of Use:

MIT

## Use Case:

External users ask an agent for Islamic prayer times, Suhoor and Iftar times, Hijri dates, and Ramadan calendars for a city or coordinates worldwide.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided locations may be interpolated into documented shell commands without safe encoding.

Mitigation: Review commands before execution and pass city, country, and coordinate values through URL encoding, a structured HTTP client, or curl --data-urlencode.

Risk: The skill sends requested city, country, or coordinate values to the external Aladhan Prayer Times API.

Mitigation: Avoid submitting sensitive location details and disclose that prayer-time lookups require a read-only HTTPS request to api.aladhan.com.

## Reference(s):

- [Aladhan Prayer Times API](https://aladhan.com/prayer-times-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown tables and concise text with optional inline curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local prayer times, Hijri dates, Suhoor and Iftar notes, calculation-method choices, and Ramadan calendar rows.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
