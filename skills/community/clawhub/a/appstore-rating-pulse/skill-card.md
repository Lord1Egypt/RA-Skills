## Description:

Monitor App Store ratings for any iOS app across multiple countries. Fetches live overall ratings using Apple's free iTunes Lookup API - no API key needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aligurelli](https://clawhub.ai/user/aligurelli)

### License/Terms of Use:


## Use Case:

App developers and product teams use this skill to monitor public App Store ratings for configured iOS apps across selected countries, either as an instant snapshot or a scheduled daily report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local shell script that makes HTTPS requests to Apple's public lookup API for configured app IDs and countries.

Mitigation: Review the configured app IDs and country codes before execution.

Risk: The optional cron setup creates recurring rating reports.

Mitigation: Enable the schedule only when recurring reports are needed and keep it limited to this script.

## Reference(s):

- [Apple iTunes Lookup API endpoint](https://itunes.apple.com/lookup)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text rating report with Markdown setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ratings are reported per configured app and country; N/A indicates no available rating.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
