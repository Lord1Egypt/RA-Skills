## Description: <br>
Monitors disk space and inode usage on specified paths, alerting when set thresholds are exceeded to help prevent disk-full issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nidalghETF](https://clawhub.ai/user/nidalghETF) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and infrastructure agents use this skill to check disk and inode usage on configured paths and trigger alerts when thresholds are exceeded. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled disk checks and notifications can create unexpected alerts if paths, thresholds, cron frequency, or destinations are misconfigured. <br>
Mitigation: Confirm monitored paths, usage thresholds, schedule frequency, and alert destination before enabling the skill. <br>


## Reference(s): <br>
- [Disk Usage Watcher on ClawHub](https://clawhub.ai/nidalghETF/disk-usage-watcher) <br>
- [Publisher profile: nidalghETF](https://clawhub.ai/user/nidalghETF) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Shell commands] <br>
**Output Format:** [Structured status and details object with disk usage entries and alert information] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configurable usage thresholds, inode thresholds, monitored paths, and alert-on-failure behavior.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
