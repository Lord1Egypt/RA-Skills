## Description: <br>
AgentMesh provides encrypted, authenticated messaging between AI agents using cryptographic identities, local or TCP hubs, and optional persistent keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cerbug45](https://clawhub.ai/user/cerbug45) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use AgentMesh to add encrypted message routing, peer discovery, and persistent agent identities to Python-based agent systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Network mode may be exposed too broadly and lacks clear transport and authentication safeguards for the security claims it makes. <br>
Mitigation: Use local mode for experiments; for network mode, bind to localhost or a private interface and place the hub behind firewall or VPN controls. <br>
Risk: Public internet exposure could allow unwanted access to the hub service. <br>
Mitigation: Avoid exposing the hub directly to the public internet and restrict network access to trusted hosts. <br>
Risk: Peer identity or persistent key handling mistakes can weaken message trust. <br>
Mitigation: Verify peer fingerprints out of band and protect persistent key files with restrictive permissions or secret storage. <br>


## Reference(s): <br>
- [ClawHub AgentMesh skill page](https://clawhub.ai/cerbug45/agentmesh) <br>
- [README](artifact/README.md) <br>
- [Full usage guide](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces implementation guidance and runnable Python examples for local and networked agent messaging.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
