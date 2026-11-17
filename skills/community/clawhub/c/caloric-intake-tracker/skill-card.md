## Description:

Log and track daily calorie intake, macronutrients, body weight, and waist measurements locally in a SQLite database, with daily and weekly statistics, rolling averages, and future calorie budgets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patello](https://clawhub.ai/user/patello)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to record food intake, body measurements, goals, and completion status in a local tracker. It supports health coaching and personal tracking workflows by producing local CLI commands and readable reports for daily, weekly, trend, weight, waist, and custom measurement views.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores food, weight, waist, and related notes in a local SQLite database that may contain sensitive health data.

Mitigation: Choose a private database location with --database, track where health_data.db is created, and manage file permissions and backups accordingly.

Risk: Generated log commands can include stored food names from the local database, which may be unsafe to copy if existing database content is untrusted or unusual.

Mitigation: Review generated Log command output before pasting or running it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/patello/skills/caloric-intake-tracker)
- [Publisher Profile](https://clawhub.ai/user/patello)
- [Skill Documentation](artifact/SKILL.md)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for a local Python CLI and local SQLite database; no external service output is produced.]

## Skill Version(s):

1.4.4 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
