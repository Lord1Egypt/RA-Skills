## Description:

Inspect Honeybadger projects, faults (error groups), fault details, and notices (error occurrences) through the bundled GET-only BadgerPeek CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivankuznetsov](https://clawhub.ai/user/ivankuznetsov)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support engineers use BadgerPeek to inspect recent Honeybadger projects, error groups, fault details, and occurrences without using Honeybadger MCP, Docker, or mutation-capable API clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Honeybadger credentials could be sent to an unintended HTTPS or loopback endpoint if endpoint environment variables are changed.

Mitigation: Use a minimally scoped read-only token and set HONEYBADGER_API_URL or HONEYBADGER_ENDPOINT only for a trusted Honeybadger endpoint that is intentionally used.

Risk: Honeybadger project names, error context, and stack data may contain sensitive operational information.

Mitigation: Limit output to fields needed for the investigation and avoid reproducing unnecessary response data.

## Reference(s):

- [BadgerPeek on ClawHub](https://clawhub.ai/ivankuznetsov/skills/badgerpeek)
- [Publisher profile](https://clawhub.ai/user/ivankuznetsov)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include redacted Honeybadger response data; users should avoid reproducing unnecessary sensitive fields.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
