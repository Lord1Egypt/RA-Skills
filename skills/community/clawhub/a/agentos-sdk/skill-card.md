## Description: <br>
AgentOS SDK provides APIs and CLI tools for persistent AI agent memory, project and task management, activity logging, inter-agent communication, and self-evolution workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AgentOSsoftware](https://clawhub.ai/user/AgentOSsoftware) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to connect agents to AgentOS for persistent memory, searchable recall, project and task tracking, activity logs, mesh communication, and recurring operational routines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill defaults to insecure transport for AgentOS endpoints. <br>
Mitigation: Use only a trusted HTTPS AgentOS endpoint and avoid the raw-IP HTTP default. <br>
Risk: Recurring memory sync can transmit sensitive conversation notes, credentials, customer data, or confidential project context. <br>
Mitigation: Apply least-privilege and rotated API keys, review what is synced, and do not automatically sync raw sensitive context. <br>
Risk: Webhooks, WebSockets, mesh communication, and bulk export are high-trust features. <br>
Mitigation: Enable these features only with clear tenant, retention, and access-control expectations. <br>


## Reference(s): <br>
- [AgentOS SDK ClawHub page](https://clawhub.ai/AgentOSsoftware/agentos-sdk) <br>
- [AgentOS website](https://agentos.software) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include AgentOS API endpoint configuration, API-key environment variables, memory paths, tags, mesh commands, and operational routines.] <br>

## Skill Version(s): <br>
3.7.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
