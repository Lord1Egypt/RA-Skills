## Description: <br>
Real-time AI API usage tracking and cost monitoring for OpenClaw across multiple providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fumarole16-afk](https://clawhub.ai/user/fumarole16-afk) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to monitor AI API spend, provider balances, and active session usage through a local dashboard and agent-readable usage files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw session and configuration data for billing calculations. <br>
Mitigation: Install only when local usage monitoring is intended and limit file access to the expected OpenClaw billing paths. <br>
Risk: Billing APIs and dashboard data may be exposed without strong server-side authentication. <br>
Mitigation: Keep port 8003 and any published billing files private; add server-side authentication before exposing the dashboard beyond a trusted host. <br>
Risk: The installer can create persistent services and fetch remote code during setup. <br>
Mitigation: Review the installer before execution and provide explicit controls for starting, stopping, and deleting collected billing data. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/fumarole16-afk/ai-bill-clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and file path references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to read local usage JSON, update balance configuration, or check background service health.] <br>

## Skill Version(s): <br>
2.2.5 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
