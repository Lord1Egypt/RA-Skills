## Description: <br>
Agent Link Local Agent helps OpenClaw agents on different machines communicate through a relay server with signed messages, reconnect support, and local message handlers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericshpych](https://clawhub.ai/user/ericshpych) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure a local OpenClaw agent client that connects to a trusted relay, sends messages to local or remote agents, and registers handlers for incoming messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Relay traffic and message delivery depend on the configured relay server, so a malicious or misconfigured relay can expose or alter communication behavior. <br>
Mitigation: Use only trusted relays, prefer wss:// with valid TLS certificates, and avoid sending sensitive content unless end-to-end encryption is added. <br>
Risk: The local client uses a shared secret for message signing and relay registration. <br>
Mitigation: Keep the shared secret out of version control, rotate it when exposed, and store it in an appropriate secret manager or protected local configuration. <br>
Risk: Incoming relay messages may trigger local agent handlers. <br>
Mitigation: Review message handlers before deployment and validate sender, target, and message content before performing local actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ericshpych/agent-link-local-agent) <br>
- [Publisher profile](https://clawhub.ai/user/ericshpych) <br>
- [Local agent installation guide](docs/install-agent.md) <br>
- [Skill README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with Python snippets, shell commands, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, OpenClaw, and a trusted WebSocket relay configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
