## Description: <br>
Agent Attestation is a portable reputation system for agents with Ed25519 signatures, input validation, and handoff key-value storage. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[nantes](https://clawhub.ai/user/nantes) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to create and inspect experimental signed reputation attestations, trust scores, and persisted identity handoffs for agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence flags the trust claims and local key storage as materially unsafe for security-sensitive decisions. <br>
Mitigation: Use only as experimental identity or reputation tooling until the publisher documents the trust model, fixes verification concerns, and protects keys and identity records. <br>
Risk: Private keys and identity records are stored on the local filesystem. <br>
Mitigation: Use secure storage locations, restrict filesystem permissions, and encrypt identity or key material at rest before production-like use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nantes/agent-attestation) <br>


## Skill Output: <br>
**Output Type(s):** [Code, JSON, Guidance, Configuration] <br>
**Output Format:** [Python modules with JSON attestation, verification, score, and key-value handoff records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the cryptography library, and filesystem access; stores local key and identity records.] <br>

## Skill Version(s): <br>
3.0.2 (source: server release metadata; artifact frontmatter says 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
