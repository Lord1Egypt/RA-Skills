## Description:

Energy Tracker helps an agent collect daily energy status, save entries, generate trend charts, and analyze multi-day wellness patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[martinashes](https://clawhub.ai/user/martinashes)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to record daily mental-energy check-ins, store a local JSON journal, generate PNG trend charts, and summarize multi-day wellness patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill records and analyzes mental-health-adjacent daily status data without clear consent, retention, or deletion controls.

Mitigation: Use it only after clear opt-in, and define where ./energy_data.json is stored, who can access it, how long it is retained, and how it can be deleted.

Risk: Charts and psychological labels may be mistaken for clinical assessment or medical advice.

Mitigation: Present outputs as wellness journaling, not diagnosis, and encourage professional support when the user reports sustained or urgent distress.

Risk: Proactive daily check-ins can be intrusive if the user has not explicitly enabled them.

Mitigation: Keep proactive check-ins disabled unless the user opts in, and limit collection to once per day.

## Reference(s):

- [Data Format](references/data-format.md)
- [Sample Data](references/sample-data.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, JSON records, JSON analysis output, and PNG chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores daily entries in ./energy_data.json and can generate ./energy_chart.png.]

## Skill Version(s):

1.1.0 (source: server release metadata and manifest.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
