## Description: <br>
Bot Status API deploys a lightweight Node.js status service that exposes an OpenClaw bot's runtime health, service connectivity, cron jobs, installed skills, and host metrics as JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suspect80](https://clawhub.ai/user/suspect80) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to set up a private monitoring endpoint or dashboard data source for OpenClaw agents. It helps check bot uptime, heartbeat state, configured service health, email status, Docker containers, dev servers, installed skills, cron jobs, and system resource usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The status API can expose detailed bot, service, and host information if reachable by untrusted users. <br>
Mitigation: Keep the service bound to localhost or place it behind authentication; do not expose /status publicly. <br>
Risk: Configured service and email checks can execute administrator-provided shell commands. <br>
Mitigation: Use administrator-controlled config only and review every command check before enabling the persistent service. <br>
Risk: The service disables TLS certificate verification globally for Node.js outbound requests. <br>
Mitigation: Remove or narrow the global TLS bypass before production use, especially for remote services. <br>
Risk: Skill directory scanning reads local skill files and checks required binaries. <br>
Mitigation: Avoid scanning untrusted skill directories and restrict configured paths to expected OpenClaw locations. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Skill Definition](SKILL.md) <br>
- [Example Configuration](config.example.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/suspect80/bot-status-api) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON, JavaScript, shell, and systemd configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance for a JSON HTTP status API; the deployed service returns cached JSON from /status and simple JSON from /health.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
