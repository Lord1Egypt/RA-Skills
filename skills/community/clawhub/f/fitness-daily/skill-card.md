## Description:

Fitness Daily turns a daily fitness habit into a four-group, 15-item checklist that records completed items, calculates completion rate, reports status, tracks trends, and suggests focus areas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and agents use this skill to run a daily fitness self-discipline checklist, save local check-in records, generate daily reports, summarize status, and review multi-day completion trends. It is personal habit tracking and does not provide medical, nutrition, or training advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checklist could be mistaken for professional medical, nutrition, or training advice.

Mitigation: Treat outputs as personal habit tracking only and consult a qualified professional for health conditions, injuries, diet changes, or training plans.

Risk: The skill writes fitness check-in data to a local CSV file.

Mitigation: Review the default path ~/.fitness-daily.csv or pass --log to choose where records are stored.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwumit/skills/fitness-daily)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Command-line text reports with local CSV log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates ~/.fitness-daily.csv by default, or a user-selected CSV file when --log is provided.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
