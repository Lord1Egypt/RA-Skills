## Description: <br>
Monitors the OpenClaw gateway every 3 hours, automatically restarts it when unresponsive, diagnoses startup issues, and rotates logs with 7-day retention. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shirley6692026](https://clawhub.ai/user/shirley6692026) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to keep a local OpenClaw gateway available by installing an unattended monitor that checks status, restarts failed services, logs activity, and rotates old logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs an unattended recurring watchdog for a local OpenClaw gateway. <br>
Mitigation: Review the cron entry and gateway_monitor.sh before installation, and confirm how to remove or disable the scheduled job. <br>
Risk: The monitor can restart the gateway and terminate matching OpenClaw gateway processes. <br>
Mitigation: Use it only on machines where automatic restarts and broad process termination are acceptable, and avoid shared or production hosts unless this behavior is approved. <br>
Risk: The security verdict is suspicious because the release gives limited user-control and safety documentation for unattended service control. <br>
Mitigation: Treat installation as privileged operational automation, review the logs after deployment, and keep a manual recovery path available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shirley6692026/gateway-monitor-auto-restart) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup and operation guidance for cron-based local gateway monitoring; installed scripts write logs under ~/.openclaw/logs/.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
