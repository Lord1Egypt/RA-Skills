## Description: <br>
A strict binary communication protocol for high-density, agent-to-agent interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentandbot-design](https://clawhub.ai/user/agentandbot-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to configure agents for compact binary agent-to-agent messaging, opcode handling, and offline oversight of protocol traffic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Opaque binary swarm messaging can make agent behavior difficult to audit in transit. <br>
Mitigation: Require human-readable logs or decompiled traces before deployment and review those logs during operation. <br>
Risk: Dynamic opcode or skill-definition updates can change agent behavior without enough review controls. <br>
Mitigation: Require human approval for new opcodes and skill definitions before agents accept or broadcast them. <br>
Risk: The referenced abl.one canonical contract is missing from the artifact evidence. <br>
Mitigation: Do not enable the protocol until the abl.one contract is supplied and reviewed. <br>
Risk: Swarm broadcasting may expand the impact of malformed or unsafe protocol messages. <br>
Mitigation: Keep swarm broadcasting disabled unless it is explicitly needed and reviewed for the deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentandbot-design/dil) <br>
- [README.md](README.md) <br>
- [ClawSpeak Protocol Specification v1.0 (ABL.ONE)](spec.md) <br>
- [UMP v0.1 Specification](ump/protocol.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Binary protocol frames] <br>
**Output Format:** [Markdown guidance with binary frame specifications and examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Frames use compact agent IDs, opcodes, payload arguments, and CRC32 integrity checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, manifest, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
