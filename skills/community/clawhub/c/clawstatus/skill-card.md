## Description: <br>
ClawStatus provides a real-time dashboard for monitoring OpenClaw devices, agents, sessions, cron jobs, models, and token usage with English and Chinese interface support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NeverChenX](https://clawhub.ai/user/NeverChenX) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators of OpenClaw deployments use ClawStatus to inspect runtime health, device and agent activity, sessions, scheduled jobs, model configuration, and token usage from a web dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented run command binds the dashboard to 0.0.0.0, and security evidence identifies administrative OpenClaw controls that may be unauthenticated. <br>
Mitigation: Run the service on 127.0.0.1 by default or place it behind strong authentication, VPN, or firewall controls before exposing it beyond a trusted host. <br>
Risk: Dashboard actions can modify OpenClaw configuration or trigger cron operations. <br>
Mitigation: Install only from a trusted publisher after code review, and operate it with least-privilege host and network access appropriate for an administrative console. <br>


## Reference(s): <br>
- [ClawStatus ClawHub listing](https://clawhub.ai/NeverChenX/clawstatus) <br>
- [OpenClaw project](https://github.com/anthropics/OpenClaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The deployed dashboard serves web UI and JSON API status data for an OpenClaw environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
