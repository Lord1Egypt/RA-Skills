## Description: <br>
Three-tier system health monitoring for OpenClaw with L1, L2, and L3 checks, heartbeat reporting, internationalization support, and console output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[carloscbrls](https://clawhub.ai/user/carloscbrls) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect local OpenClaw host health, run fast definition-file checks, schedule hourly system checks, and perform daily system audits on Linux or macOS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled health checks inspect local host status and can write recurring logs when crontab examples are enabled. <br>
Mitigation: Review schedules, thresholds, and log paths before enabling cron, and route logs to an intended workspace with appropriate retention. <br>
Risk: Daily audits check package-update status and estimate temporary or cache directory sizes. <br>
Mitigation: Run the audit manually first, confirm the inspected directories are appropriate for the host, and use the skill only on trusted local systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/carloscbrls/cc3po-system-healthcheck) <br>
- [Project homepage](https://github.com/cc3po/system-healthcheck) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and plain-text or JSON command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Console-oriented health-check results; optional quiet mode returns exit status only.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
