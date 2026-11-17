## Description:

Garmin Connect Pro lets an agent retrieve Garmin Connect activity, sleep, heart rate, stress, body battery, training, VO2 max, race prediction, chart, comparison, JSON export, and FIT/GPX activity data for OpenClaw workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drpeterkalmar](https://clawhub.ai/user/drpeterkalmar)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query, summarize, compare, chart, export, and download Garmin Connect health and activity data through OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive Garmin health-account access and locally cached OAuth tokens.

Mitigation: Review before installing, protect cached tokens, and remove them when no longer needed.

Risk: The skill supports a plaintext credentials file fallback.

Mitigation: Prefer secure environment variables or a credential manager, and avoid the credentials.json option when possible.

Risk: Cron or OpenClaw cron commands can expose Garmin passwords if secrets are placed directly in scheduled commands.

Mitigation: Do not put GARMIN_PASSWORD directly in cron commands; use secure environment injection or a dedicated Garmin account where possible.

Risk: The skill relies on the third-party garminconnect dependency for Garmin API communication.

Mitigation: Pin or audit the garminconnect dependency before use in sensitive environments.

## Reference(s):

- [Garmin Connect Pro on ClawHub](https://clawhub.ai/drpeterkalmar/skills/garmin-connect-pro)
- [garminconnect Python library](https://github.com/cyberjunkie/garminconnect)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, files, guidance]

**Output Format:** [Terminal text and Markdown guidance with optional JSON output and FIT/GPX file downloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, garminconnect, Garmin credentials, and locally cached OAuth tokens after login.]

## Skill Version(s):

1.4.1 (source: server release evidence; artifact SKILL.md reports 1.4.0 and package.json reports 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
