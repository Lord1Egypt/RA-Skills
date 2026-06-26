## Description: <br>
Connect Claude Code to AgentID for persistent shared memory, live activity reporting, and multi-agent mission coordination via MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[colapsis](https://clawhub.ai/user/colapsis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect Claude Code to AgentID so an agent can maintain shared memory, report task activity, and coordinate work across multiple agent instances. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to send detailed task activity to AgentID and store persistent shared memory. <br>
Mitigation: Install only when the service's access controls and retention are acceptable, redact sensitive task details, and require user confirmation before storing personal or secret information. <br>
Risk: Remote mission handoffs could influence agent behavior across shared identities. <br>
Mitigation: Review handoff content before acting on it and require user confirmation before taking sensitive or irreversible actions based on remote handoffs. <br>


## Reference(s): <br>
- [AgentID homepage](https://agentid.live) <br>
- [AgentID dashboard and Agency view](https://agentid.live/app/studio) <br>
- [AgentID docs and SDK](https://agentid.live/app/developers) <br>
- [ClawHub release page](https://clawhub.ai/colapsis/agentid-mcp) <br>
- [Publisher profile](https://clawhub.ai/user/colapsis) <br>


## Skill Output: <br>
**Output Type(s):** [Configuration, Guidance, Shell commands, JSON] <br>
**Output Format:** [Markdown with JSON configuration examples and session protocol guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides MCP setup and routine tool usage for memory, activity reporting, and mission handoffs.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
