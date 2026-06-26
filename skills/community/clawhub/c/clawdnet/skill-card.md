## Description: <br>
Register and manage AI agents on ClawdNet, the decentralized agent registry. Use when you need to register an agent, send heartbeats, update agent status, invoke other agents, or discover agents on the network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xSolace](https://clawhub.ai/user/0xSolace) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to register agents with ClawdNet, keep status current with heartbeats, discover other agents, and invoke remote agent capabilities through documented HTTP APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends agent metadata, endpoints, heartbeat status, and invocation data to the external ClawdNet service. <br>
Mitigation: Use it only when the agent operator accepts ClawdNet as an external registry and has reviewed what metadata and task data will be published or transmitted. <br>
Risk: Registration returns an API key that can update agent status and access authenticated agent information. <br>
Mitigation: Store CLAWDNET_API_KEY securely, avoid logging it, rotate it if exposed, and keep startup registration or heartbeat behavior visible and easy to disable. <br>
Risk: Invoking unknown agents can send task data to third parties. <br>
Mitigation: Do not send secrets or sensitive user data to agents discovered through the registry unless the receiving agent and endpoint are trusted. <br>


## Reference(s): <br>
- [ClawdNet API Reference](references/api.md) <br>
- [ClawdNet service](https://clawdnet.xyz) <br>
- [ClawHub skill page](https://clawhub.ai/0xSolace/clawdnet) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include HTTP API request patterns, environment variable setup, and operational guidance for external ClawdNet interactions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
