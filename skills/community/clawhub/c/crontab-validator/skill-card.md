## Description: <br>
Validate, explain, lint, and calculate next run times for cron expressions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check cron syntax, explain schedules, identify common scheduling mistakes, and calculate upcoming run times before relying on a crontab entry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a bundled local Python helper for cron analysis. <br>
Mitigation: Install it only in environments where local helper scripts are permitted and review the artifact and security summary before use. <br>
Risk: Cron guidance may be copied into production schedules without confirming operational impact. <br>
Mitigation: Treat cron expressions as data, review the explanation and lint findings, and test schedules before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/crontab-validator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text, JSON, or Markdown produced by cron validation, explanation, lint, and next-run commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can process one or more cron expressions and include lint findings, field-level explanations, or next run times.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
