## Description:

Validate, explain, lint, and calculate next run times for cron expressions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and other external users use this skill to check cron syntax, explain schedules, calculate upcoming run times, and lint common cron mistakes before using crontab entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a local executable helper script for cron syntax and schedule analysis.

Mitigation: Review release changes and scan the script before upgrading or deploying it in managed environments.

Risk: Cron linting and next-run calculations can miss operational context such as job side effects, host timezone policy, or production load.

Mitigation: Treat validation results as schedule analysis and separately review the actual job behavior, timezone, and execution environment before production use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Text, JSON, or Markdown command output with cron explanations, validation results, lint findings, and next-run schedules.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local command-line helper; supports validate, explain, next, and lint modes.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
