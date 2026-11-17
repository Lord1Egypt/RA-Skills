## Description:

Agent-to-agent discovery network. Register agents with capability cards, discover peers by skill/domain, perform trust-scored handshakes, and run a FastAPI discovery server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cassh100k](https://clawhub.ai/user/cassh100k)

### License/Terms of Use:


## Use Case:

Developers and agent builders use AgentNet to register agents, publish capability cards, discover peers by skill or domain, and exercise a trust-scored handshake flow for multi-agent collaboration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The discovery server exposes registry and handshake controls without adequate authentication, authorization, privacy boundaries, or real identity verification.

Mitigation: Use only for local experimentation or on a protected development network; add authentication, authorization, signed identity verification, deletion controls, and audit logging before public deployment.

Risk: Registered agent contact data, personal handles, production identities, endpoints, secrets, or credentials could be exposed through registry or discovery flows.

Mitigation: Do not register real endpoints, secrets, personal handles, production agent identities, or credentials until redaction and privacy controls are implemented.

## Reference(s):

- [AgentNet ClawHub Release](https://clawhub.ai/cassh100k/skills/agentnet)
- [Publisher Profile](https://clawhub.ai/user/cassh100k)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with Python and shell command examples; FastAPI endpoints return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local server setup, registry operations, agent card generation, and handshake examples.]

## Skill Version(s):

0.1.0 (source: server release metadata, artifact manifest, and package changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
