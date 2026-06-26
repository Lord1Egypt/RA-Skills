## Description: <br>
Use when building an AI agent that needs to communicate with other agents over the Agent2Agent (A2A) protocol, publishing an AgentCard for discovery, acting as an A2A client or server, or integrating A2A capabilities into an existing agent framework. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjipeng977](https://clawhub.ai/user/wangjipeng977) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to understand A2A protocol concepts, publish AgentCards, and implement task delegation, streaming updates, push notifications, and local protocol experiments for agent-to-agent collaboration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task text, files, metadata, callback URLs, and artifacts may be sent to remote agents during A2A interactions. <br>
Mitigation: Use the skill only for intended A2A connections, validate target AgentCards and authentication requirements, and avoid sending sensitive task content to untrusted agents. <br>
Risk: The optional mock server exposes a local network service and can forward task data to webhook URLs. <br>
Mitigation: Run the mock server only in a trusted local environment, prefer loopback-only binding, and do not accept webhook or push-provider URLs from untrusted callers. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wangjipeng977/a2a-agent-protocol) <br>
- [A2A Protocol Specification](https://a2a-protocol.org/latest/specification/) <br>
- [A2A GitHub Project](https://github.com/a2aproject/A2A) <br>
- [A2A Python SDK](https://github.com/a2aproject/a2a-python) <br>
- [A2A Protocol Overview](references/a2a-overview.md) <br>
- [A2A Data Model Reference](references/data-model.md) <br>
- [A2A Operations Reference](references/operations.md) <br>
- [AgentCard Template Reference](references/agent-card-template.md) <br>
- [A2A Quickstart](references/quickstart.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON examples, shell commands, and generated AgentCard JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start a local mock A2A HTTP server when the host supports Python execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
