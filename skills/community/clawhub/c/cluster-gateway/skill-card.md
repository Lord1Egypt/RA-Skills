## Description: <br>
Manages the OpenClaw Cluster Gateway as a central hub for sub-agent communication, task distribution, and cluster coordination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kikikari](https://clawhub.ai/user/kikikari) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cluster operators use this skill to check an OpenClaw gateway, deploy sub-agents to nodes, dispatch tasks to workers, and configure relay nodes. The artifact notes that the messaging interface is still pending, so operational use should account for that blocker. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gateway commands can target the wrong node, agent type, or task text if copied without review. <br>
Mitigation: Confirm the target node, agent type, and task text before running documented commands. <br>
Risk: Exposing the gateway port to untrusted networks can create unauthorized access risk. <br>
Mitigation: Use authentication, TLS, firewalling, and node allowlisting before exposing the gateway beyond trusted networks. <br>
Risk: The artifact identifies the messaging interface as pending, which may block complete cluster operation. <br>
Mitigation: Treat messaging-dependent workflows as incomplete until the interface is selected, tested, and documented. <br>


## Reference(s): <br>
- [Cluster Gateway Skill Page](https://clawhub.ai/kikikari/cluster-gateway) <br>
- [Worker Node Skill](../worker-node/SKILL.md) <br>
- [Relay Node Skill](../relay-node/SKILL.md) <br>
- [Resource Manager Skill](../resource-manager/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documents gateway status checks, deployment commands, task dispatch commands, relay configuration, node roles, and sample gateway configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
