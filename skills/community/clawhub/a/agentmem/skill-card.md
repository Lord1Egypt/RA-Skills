## Description: <br>
Cloud memory for AI agents. Writes are free, pay only for reads. First 25 calls free, 7-day persistence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NatMota](https://clawhub.ai/user/NatMota) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent builders use AgentMem to store, retrieve, delete, and optionally share cloud-hosted agent memories across sessions and devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent memories may be automatically stored with a third-party cloud service. <br>
Mitigation: Use the skill only where third-party memory storage is approved, and avoid storing credentials, secrets, private user details, business data, or raw conversation context. <br>
Risk: No-key demo mode and demo workflows can create real persisted data. <br>
Mitigation: Use synthetic data for demos and avoid no-key mode for real or sensitive data. <br>
Risk: Public memory sharing can expose stored content beyond the intended agent workflow. <br>
Mitigation: Disable public=true and scheduled memory sync unless explicit approval, retention expectations, deletion behavior, and sharing consequences are understood. <br>


## Reference(s): <br>
- [AgentMem API](https://api.agentmem.io/v1) <br>
- [AgentMem website](https://agentmem.io) <br>
- [ClawHub skill page](https://clawhub.ai/NatMota/agentmem) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON API payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides agents to call AgentMem HTTP endpoints and may include API key, source, and agent-name headers.] <br>

## Skill Version(s): <br>
2.4.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
