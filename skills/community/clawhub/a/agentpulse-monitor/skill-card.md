## Description: <br>
AI-powered infrastructure monitoring - thin agent, smart cloud. One-command install, real-time alerts, baseline learning, auto-remediation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[strouddustinn-bot](https://clawhub.ai/user/strouddustinn-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to install and operate a Linux monitoring agent that reports service, resource, process, port, and uptime data to AgentPulse for alerting and dashboard review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review identifies deployment and transport-security risks before use on real servers. <br>
Mitigation: Review the agent carefully before installation and do not use it on production or sensitive hosts until TLS verification is enabled. <br>
Risk: The install flow includes a pipe-to-bash installer and cron entry setup. <br>
Mitigation: Inspect and verify the downloaded installer independently, and review cron entries before installing or enabling scheduled reports. <br>
Risk: The agent requires API credentials and reports host telemetry to a cloud service. <br>
Mitigation: Protect the API key configuration and confirm what telemetry AgentPulse stores, how long it is retained, and who can access it. <br>


## Reference(s): <br>
- [AgentPulse documentation](https://agentpulse.io/docs) <br>
- [AgentPulse dashboard](https://agentpulse.io/dashboard) <br>
- [ClawHub skill page](https://clawhub.ai/strouddustinn-bot/agentpulse-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes installation, cron scheduling, API usage, and monitoring configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
