## Description:

Portable reputation system for agents v3 with Ed25519 signatures, input validation, and handoff KV storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nantes](https://clawhub.ai/user/nantes)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to create and verify signed agent attestations, compute reputation-style trust scores, and persist identity or reputation data across handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local file writes may place keys, attestations, and KV data in unsafe or shared directories.

Mitigation: Use protected absolute storage paths with restrictive permissions before running the system outside a test environment.

Risk: Private keys and identity data may be stored without encryption at rest.

Mitigation: Encrypt sensitive key and identity material at rest and avoid storing it in shared workspace or credential directories.

Risk: Agent reputation and trust claims may be treated as authoritative even though enforcement is inconsistent.

Mitigation: Require human review before using attestations for real trust decisions, and constrain agent identifiers to safe, expected values.

Risk: Legacy v1 and v2 modules remain in the artifact alongside the v3 implementation.

Mitigation: Remove or clearly disable legacy modules before release use so operators do not rely on weaker or outdated behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nantes/skills/agent-attestation)
- [Publisher profile](https://clawhub.ai/user/nantes)

## Skill Output:

**Output Type(s):** [Code, Files, Guidance]

**Output Format:** [Python modules that produce JSON-compatible attestation, verification, trust score, and KV data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, the cryptography library, and filesystem access; writes local key and KV files.]

## Skill Version(s):

3.0.2 (source: server release metadata; artifact frontmatter reports 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
