## Description:

Real-time flight operations center for delays, cancellations, gate changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kurosh87](https://clawhub.ai/user/kurosh87)

### License/Terms of Use:


## Use Case:

Travelers and travel operations agents use this skill to monitor upcoming flights, triage delays, cancellations, gate changes, and connection risks, and prepare recovery options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store recent flight alert activity in ~/alert-history.json, which can contain sensitive flight metadata.

Mitigation: Inspect, protect, or delete the local alert-history file according to the user's privacy requirements.

Risk: The skill can prepare rebooking actions after cancellations or missed connections.

Mitigation: Require explicit user authorization before any booking action is submitted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kurosh87/skills/aerobase-alerts)
- [ClawHub Publisher Profile](https://clawhub.ai/user/kurosh87)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration, Text]

**Output Format:** [Markdown with concise operational recommendations and API endpoint references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain a short local flight-alert history in ~/alert-history.json for notification deduplication.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
