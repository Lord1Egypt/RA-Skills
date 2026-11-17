## Description:

Query Apple Health data exported as CSV files from iOS apps, with local summaries and metric queries for heart rate, steps, sleep, blood oxygen, workouts, body measurements, and related health data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to inspect Apple Health CSV exports locally, summarize recent health metrics, and query trends such as heart rate, steps, sleep, blood oxygen, workouts, and body measurements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apple Health CSV exports can contain sensitive health information.

Mitigation: Use only CSV exports the user intentionally provides, keep the export directory protected, and avoid syncing or sharing raw CSV files unless the user accepts the privacy risk.

Risk: Generated summaries can disclose sensitive health details from the source CSVs.

Mitigation: Review generated summaries before sharing them and treat them with the same privacy controls as the underlying Apple Health export.

Risk: Some displayed metric names are in Chinese, which may reduce interpretability for some users.

Mitigation: Confirm metric meanings against the supported metric table or JSON metric keys before relying on a summary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lanyasheng/skills/apple-health-csv)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON CLI output, with Markdown usage guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally against user-provided CSV files; no API keys or cloud services are described.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
