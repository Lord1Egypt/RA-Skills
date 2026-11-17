## Description:

Convert between Unix epoch timestamps in seconds or milliseconds and human-readable date strings in any IANA timezone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and other external users use this skill to convert Unix timestamps to readable datetimes, or date/time strings back to epoch values, while preserving explicit timezone context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A short timezone phrase or ambiguous timestamp request may cause the skill to run when the user meant a different conversion or timezone.

Mitigation: Confirm the conversion direction, timestamp unit, and IANA timezone before relying on the result.

Risk: Timezone-naive date strings are interpreted using the supplied timezone, and missing timezone context can lead to an incorrect epoch value.

Mitigation: Require a timezone for date-to-epoch conversion and disclose UTC when it is used as the default for epoch-to-date conversion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/epoch-time-converter)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and one-line CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns either a converted datetime with timezone context or an epoch value in seconds or milliseconds.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
