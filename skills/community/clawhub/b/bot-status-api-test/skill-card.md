## Description: <br>
Deploy a lightweight status API that exposes an OpenClaw bot's runtime health, service connectivity, cron jobs, skills, system metrics, and related status data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suspect80](https://clawhub.ai/user/suspect80) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to set up a JSON status endpoint or monitoring dashboard for an OpenClaw agent, including service checks, cron visibility, skill inventory, and host metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The status API may expose host, OpenClaw workspace, cron, skill, model, context, and service telemetry to unintended audiences. <br>
Mitigation: Bind the API to localhost or protect it with strong authentication and TLS before making it reachable from a network. <br>
Risk: Configured command-based health checks can execute shell commands on the host. <br>
Mitigation: Disable command checks unless every configuration source is trusted, and run the service under a low-privilege account. <br>
Risk: The release was classified as suspicious by the authoritative security evidence because scoping and access-control guidance is incomplete. <br>
Mitigation: Review the skill before installing and avoid exposing OpenClaw telemetry to untrusted networks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suspect80/bot-status-api-test) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON, shell, and systemd snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local file paths, service configuration, and deployment commands for a Node.js status API.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
