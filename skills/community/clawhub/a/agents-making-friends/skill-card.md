## Description: <br>
Enables an OpenClaw agent to call remote A2A agents or expose itself as an A2A service for agent-to-agent communication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[verylowlow](https://clawhub.ai/user/verylowlow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect OpenClaw instances or expose an OpenClaw assistant through A2A endpoints for cross-agent messaging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the server can expose a local OpenClaw agent to network callers with weak default access controls. <br>
Mitigation: Use strong authentication and run behind TLS, a VPN, or firewall controls; avoid public or shared networks unless the agent profile is restricted. <br>
Risk: Bearer tokens may be stored in markdown configuration or sent to untrusted remote agent URLs. <br>
Mitigation: Keep tokens out of markdown files and logs, and send bearer tokens only to remote A2A agents you fully trust. <br>


## Reference(s): <br>
- [A2A API Reference](artifact/references/a2a-api.md) <br>
- [A2A Specification](https://a2a-protocol.org/latest/specification/) <br>
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification) <br>
- [A2A GitHub Project](https://github.com/a2aproject/A2A) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands, Python scripts, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call remote A2A endpoints or run a local HTTP A2A service that returns JSON-RPC task responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
