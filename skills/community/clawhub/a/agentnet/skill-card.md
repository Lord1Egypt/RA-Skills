## Description: <br>
Agent-to-agent discovery network. Register agents with capability cards, discover peers by skill/domain, perform trust-scored handshakes, and run a FastAPI discovery server. Enables agents to find each other, negotiate, and form teams without human orchestration. Use when building multi-agent systems, agent marketplaces, or peer-to-peer agent collaboration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cassh100k](https://clawhub.ai/user/cassh100k) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers building multi-agent systems use AgentNet to register agents, publish capability cards, discover peers by capability, and run a handshake flow for task negotiation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unauthenticated discovery and mutation endpoints can expose or alter registry data if the service is made public. <br>
Mitigation: Run the service on localhost or behind a trusted proxy, and add authentication plus ownership checks before exposing endpoints. <br>
Risk: Agent metadata and contact endpoints may reveal sensitive operational details. <br>
Mitigation: Avoid publishing sensitive agent metadata or real contact endpoints, and review registered cards before public discovery. <br>
Risk: Fingerprint, signature, and handshake flows should not be treated as strong security controls. <br>
Mitigation: Use stronger cryptographic identity, signature, and session validation before relying on AgentNet for trust decisions. <br>


## Reference(s): <br>
- [AgentNet ClawHub Page](https://clawhub.ai/cassh100k/agentnet) <br>
- [AgentNet README](artifact/README.md) <br>
- [AgentNet Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python code references, shell commands, API examples, and JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local FastAPI registry workflow, agent card data, handshake flow guidance, and command examples.] <br>

## Skill Version(s): <br>
0.1.0 (source: clawpkg.yaml and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
