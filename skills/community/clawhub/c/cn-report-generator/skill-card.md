## Description:

Generates Chinese daily and weekly work reports from local MEMORY.md and daily log files, with documented daily, weekly, and monthly report templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers can use this skill to turn local Chinese work logs into structured daily and weekly Markdown reports. It is suited for personal or team status reporting when the underlying logs are maintained regularly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports can overwrite fixed files under ~/reports.

Mitigation: Review output paths before use and keep backups or version control for report directories where existing reports matter.

Risk: Generated business reports include unrelated branding from the artifact.

Mitigation: Inspect generated reports before sharing and remove branding that is not appropriate for the audience.

Risk: Monthly reporting is advertised but not implemented in the bundled script.

Mitigation: Use the daily and weekly report paths as implemented, and treat monthly output as unavailable until the skill is updated.

Risk: Report quality depends on the completeness of local work logs.

Mitigation: Maintain daily log files consistently and review generated summaries for omissions before relying on them.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown reports saved as local files, plus brief command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local work-log files from the user's home workspace and writes report files under ~/reports.]

## Skill Version(s):

1.2.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
