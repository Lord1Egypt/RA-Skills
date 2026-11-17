## Description:

Connects agents to Garmin Connect CN so they can query personal health, sleep, training, and activity data, analyze activity details, and export activity files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xent9312](https://clawhub.ai/user/xent9312)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents can retrieve Garmin Connect CN health, sleep, training, and activity records for user-authorized accounts. The skill also supports detailed running and activity analysis plus FIT, GPX, TCX, and CSV exports.

### Deployment Geography for Use:

China (Garmin Connect CN service)

## Known Risks and Mitigations:

Risk: The skill requires Garmin Connect CN account access and can expose sensitive health, activity, and possible GPS data.

Mitigation: Use only with user-authorized accounts, prefer a sandbox or dedicated account, and confirm intent before querying or exporting sensitive data.

Risk: Reusable Garmin credentials are stored locally for later commands.

Mitigation: Avoid entering passwords in shared terminals, inspect file permissions, and review or remove ~/.config/garmin-cn/credentials.json after use.

Risk: Login may delete the ~/.garth session cache used by other Garmin or Garth tools.

Mitigation: Run the skill in an isolated environment when other Garmin or Garth sessions must be preserved.

## Reference(s):

- [Advanced usage](references/advanced-usage.md)
- [ClawHub skill page](https://clawhub.ai/xent9312/skills/garmin-connect-cn-data)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell command examples and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can export FIT, GPX, TCX, and CSV activity files and parse FIT files into JSON.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
