## Description: <br>
AgentOS SDK for Clawdbot helps agents sync conversation context, project memory, heartbeat status, mesh messages, and dashboard data with AgentOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AgentOSsoftware](https://clawhub.ai/user/AgentOSsoftware) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to connect Clawdbot-style agents to AgentOS for persistent memory, project tracking, dashboard visibility, mesh messaging, and sync workflows. It is most relevant when ongoing cloud synchronization of active agent context is intentional and acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill syncs active conversation state, notes, project memory, and heartbeat data to the AgentOS service. <br>
Mitigation: Install only when that persistent cloud sync is intended, and confirm what data is uploaded before enabling heartbeat or automatic sync workflows. <br>
Risk: The documented default API endpoint uses an HTTP raw-IP URL and API-key authentication. <br>
Mitigation: Prefer a trusted HTTPS endpoint, verify API key scope, and confirm deletion and retention controls before storing sensitive context. <br>
Risk: Cron, daemon, and mesh wake features can create ongoing background sync or wake behavior. <br>
Mitigation: Enable those features only after reviewing operational impact, and keep them disabled when continuous background activity is not acceptable. <br>
Risk: The installer expects an aos CLI file that is not included in the provided artifact evidence. <br>
Mitigation: Inspect or obtain the missing CLI from a trusted source before running setup or relying on documented commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/AgentOSsoftware/agentos) <br>
- [AgentOS dashboard](https://brain.agentos.software) <br>
- [AgentOS docs](https://agentos.software/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup, sync, heartbeat, cron, daemon, mesh messaging, API, and troubleshooting instructions for an agent operator.] <br>

## Skill Version(s): <br>
1.4.4 (source: server release evidence and artifact SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
