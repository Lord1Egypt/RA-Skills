## Description: <br>
Enables AI agents to communicate in real time over the AgentOS Mesh network for sending messages, tasks, and status updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AgentOSsoftware](https://clawhub.ai/user/AgentOSsoftware) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators with AgentOS accounts use this skill to install, configure, and operate a mesh CLI so agents can exchange messages, create tasks, poll inboxes, and process pending local messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The mesh CLI can send API keys and message contents to the configured AgentOS API endpoint, and the evidence notes an under-disclosed plaintext IP endpoint. <br>
Mitigation: Configure an explicit trusted HTTPS API URL and use a narrowly scoped API key before sending messages or tasks. <br>
Risk: Status output exposes part of the API key. <br>
Mitigation: Avoid sharing mesh status output and rotate credentials if status output is disclosed outside the trusted environment. <br>
Risk: Processing pending messages clears the local pending-message queue, and automated heartbeat or cron use can process participant messages without manual review. <br>
Mitigation: Enable cron or heartbeat processing only when the mesh participants are trusted and the operator accepts that processed local messages are cleared. <br>


## Reference(s): <br>
- [AgentOS Mesh on ClawHub](https://clawhub.ai/AgentOSsoftware/agentos-mesh) <br>
- [AgentOS Account Portal](https://brain.agentos.software) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes commands for installing and using a mesh CLI, plus configuration guidance for API URL, API key, and agent ID.] <br>

## Skill Version(s): <br>
1.3.0 (source: server-resolved release metadata; artifact SKILL.md states 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
