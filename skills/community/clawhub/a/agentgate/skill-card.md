## Description: <br>
API gateway for personal data with human-in-the-loop write approval. Connects agents to GitHub, Bluesky, Google Calendar, Home Assistant, and more - all through a single API with safety controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[monteslu](https://clawhub.ai/user/monteslu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to connect an OpenClaw agent to an agentgate server for controlled access to personal services, service discovery, queued writes, inter-agent messaging, and persistent memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose broad personal-data and write access through connected services. <br>
Mitigation: Install it only for intentionally operated agentgate servers, restrict the API token to least privilege, and review connected services before use. <br>
Risk: Approval-bypass mode can allow writes to execute immediately. <br>
Mitigation: Keep write approval enabled unless there is a tightly scoped and audited reason to use bypass mode. <br>
Risk: Memory and inter-agent messaging may carry sensitive personal or account data. <br>
Mitigation: Review the memory and messaging configuration before allowing sensitive data through the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/monteslu/agentgate) <br>
- [Agentgate documentation](https://agentgate.org) <br>
- [Agentgate skills documentation](https://agentgate.org/docs/skills) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, markdown] <br>
**Output Format:** [Markdown with inline HTTP examples, shell commands, and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGENT_GATE_URL and AGENT_GATE_TOKEN for a configured agentgate server.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
