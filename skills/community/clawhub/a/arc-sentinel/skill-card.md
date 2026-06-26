## Description: <br>
Arc Sentinel provides security monitoring and infrastructure health checks for OpenClaw agents, including breach monitoring, SSL certificate expiry checks, GitHub security audits, credential rotation tracking, secret scanning, git hygiene, token watchdog, and permission audits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arc-claw-bot](https://clawhub.ai/user/arc-claw-bot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use Arc Sentinel to run local or scheduled security checks for agent infrastructure, review warning and critical findings, and track credential rotation status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs broad local security checks and may read credential, token, repository, and configuration metadata. <br>
Mitigation: Install and run it only in environments you are authorized to audit, and treat terminal output and JSON reports as sensitive. <br>
Risk: Breach monitoring can query HaveIBeenPwned for a monitored email address and may require a HIBP API key. <br>
Mitigation: Enable HIBP checks only for accounts you are authorized to monitor, and store the API key in local configuration with appropriate access controls. <br>
Risk: Cron or heartbeat execution can create recurring scans of repositories, credentials, domains, and account activity. <br>
Mitigation: Use recurring execution only when continuous monitoring is intended, and review sentinel.conf and credential-tracker.json before scheduling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arc-claw-bot/arc-sentinel) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Terminal reports, JSON report files, and concise agent summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit codes indicate all clear, warnings, or critical findings; reports may contain sensitive security metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
