## Description:

Collect structured Booking.com hotel records from a known Booking hotel or listing URL and return the collected results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit known Booking.com hotel or listing URLs to Dataify, monitor the collection task, and return final structured JSON results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends target Booking.com URLs and a Dataify API token to Dataify.

Mitigation: Use it only when that data sharing is acceptable, keep tokens out of chat and command arguments, and prefer session-scoped environment variables.

Risk: The Chinese localized instructions do not match the primary workflow for returning collected results.

Mitigation: Review localized instructions before use and follow the primary workflow that waits for completion and returns the final result unless no-wait behavior is explicitly requested.

Risk: The security verdict is suspicious because of credential-handling and workflow risks.

Mitigation: Review and scan the skill before installing or deploying it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-booking-hotellist)
- [ClawHub publisher profile](https://clawhub.ai/user/dataify-server)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and final JSON collection results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default behavior waits for the asynchronous task and returns the final result; no-wait behavior returns the submission response or task ID.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
