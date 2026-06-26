## Description: <br>
Enables and maintains cron-driven real-execution auto progression for the crypto-hedge-backtest project. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evanfirefly](https://clawhub.ai/user/evanfirefly) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and maintainers use this skill to set up, verify, and troubleshoot recurring cron jobs that keep the crypto-hedge-backtest project moving through real script runs, code changes, generated files, and progress reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring cron automation can keep running project scripts or changing files without clear limits. <br>
Mitigation: Require exact cron definitions before enabling jobs, set an expiration or maximum run count, and document how to pause or delete each job. <br>
Risk: Automated progress jobs may modify the crypto backtest project during unattended runs. <br>
Mitigation: Restrict allowed scripts and paths, require approval before code changes, and run the workflow on a separate branch or sandbox. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/evanfirefly/crypto-auto-progression) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with inline shell commands and cron configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
