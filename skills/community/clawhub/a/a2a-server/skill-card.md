## Description: <br>
A WebSocket-based agent-to-agent messaging server for agent registration, discovery, RPC calls, publish/subscribe messaging, heartbeats, reconnects, and offline queues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent engineers use this skill to run a local or trusted WebSocket coordination server for multi-agent messaging, RPC calls, pub/sub notifications, capability discovery, and offline message delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server can route remote agent calls without implemented authentication, authorization, TLS, or message signing. <br>
Mitigation: Run it only on localhost or trusted networks until those controls are added, and use allowlists for agent IDs and capabilities. <br>
Risk: Remote or untrusted agents could receive sensitive prompts, credentials, private code, or task data passed through the messaging server. <br>
Mitigation: Do not send secrets or sensitive payloads through agents you do not fully trust. <br>
Risk: Offline messages are queued by the server and may contain task data while agents are disconnected. <br>
Mitigation: Keep queue contents non-sensitive, limit retention, and clear queues when operating outside a fully trusted local environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/a2a-server) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [TEST-STATUS.md](TEST-STATUS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript examples, shell commands, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local server commands, environment variables, client code snippets, and security caveats.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
