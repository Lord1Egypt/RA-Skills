## Description:

AgentMesh provides encrypted, authenticated messaging between AI agents through local or TCP hubs using cryptographic identities and routed envelopes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cerbug45](https://clawhub.ai/user/cerbug45)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use AgentMesh to add local or networked message exchange between AI agents while keeping payloads encrypted from the hub. It supports agent identity, peer discovery, persistent keys, and example workflows for multi-agent and LLM-agent pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security claims may overstate the implementation's guarantees for hostile networks or production-grade forward secrecy.

Mitigation: Review the cryptographic design before sensitive use and do not rely on it for hostile-network security without further hardening.

Risk: Network hub deployments can expose routing and public-key discovery services over TCP.

Mitigation: Use LocalHub where possible, bind NetworkHubServer to localhost or private networks, and add firewalling and authenticated transport before exposing it.

Risk: Persistent key files contain long-lived private key material.

Mitigation: Store key files outside source control with restrictive filesystem permissions and treat them as secrets.

## Reference(s):

- [AgentMesh ClawHub page](https://clawhub.ai/cerbug45/skills/agentmesh)
- [Publisher profile](https://clawhub.ai/user/cerbug45)
- [README](README.md)
- [SKILL.md](SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with Python and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers local hubs, TCP hub setup, persistent key files, and API usage patterns.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
