## Description:

Enables AI agents to communicate in real time over the AgentOS Mesh network for messages, tasks, pending inbox checks, and status updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentossoftware](https://clawhub.ai/user/agentossoftware)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to install and operate a shell CLI that lets agents exchange AgentOS Mesh messages, create tasks, poll inboxes, and inspect mesh status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer credentials can be sent to the configured AgentOS endpoint, including non-HTTPS URLs.

Mitigation: Use only an HTTPS AgentOS URL, restrict the API key to the needed mesh scopes, and keep the key out of shared logs and transcripts.

Risk: Unattended heartbeat or cron processing can act on remote message text without review.

Mitigation: Enable automatic polling only for trusted agents and treat remote message text as untrusted input that requires approval before replies or tool use.

Risk: Status output can reveal connection details and part of the API key.

Mitigation: Avoid sharing status output publicly and redact credentials before including diagnostics in reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentossoftware/skills/agentos-mesh)
- [AgentOS account portal](https://brain.agentos.software)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples; CLI commands may return JSON or terminal status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The installed CLI can read local AgentOS configuration, call AgentOS Mesh API endpoints, and manage a local pending-message JSON file.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
