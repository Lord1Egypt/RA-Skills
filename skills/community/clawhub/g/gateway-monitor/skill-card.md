## Description: <br>
Provides real-time monitoring, log search, service status, alerts, and one-click config restore for OpenClaw Gateway and related services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yes999zc](https://clawhub.ai/user/yes999zc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor local OpenClaw Gateway health, search logs, inspect related service status, manage alerts, and recover configuration from backups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on external gateway-monitor server code that can control local Gateway services and configuration. <br>
Mitigation: Review and pin the external repository code before installation, especially server.js and the launchd plist. <br>
Risk: Exposing the monitoring dashboard or service-control endpoints could allow local service changes or interruptions. <br>
Mitigation: Keep the dashboard bound to 127.0.0.1, do not expose its port, and require confirmation before restore, restart, stop, or wake actions. <br>
Risk: API keys and service credentials may be used by the local monitoring workflow. <br>
Mitigation: Use least-privileged API keys and treat displayed or configured credentials as sensitive. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands, environment variables, endpoint lists, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local dashboard URLs, service-control endpoints, and configuration details for OpenClaw Gateway, LiteLLM, oMLX, and related services.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
