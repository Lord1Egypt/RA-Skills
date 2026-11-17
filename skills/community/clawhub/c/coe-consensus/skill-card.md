## Description:

Evaluate signed votes against an operator-configured quorum.

This skill is ready for commercial/non-commercial use.

## Publisher:

[schchit](https://clawhub.ai/user/schchit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run a local signed-vote quorum evaluation API for COE/JEP-style events and produce a resolved or unresolved Shared World State result. It supports simple majority, weighted trust, and BFT-style quorum policies configured by the operator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The service can be exposed beyond its intended local trust boundary.

Mitigation: Run it on loopback or behind a hardened reverse proxy with TLS, request-rate limits, read-time limits, and restricted service-account configuration.

Risk: Bearer tokens and environment configuration control tenant access and consensus permissions.

Mitigation: Use high-entropy bearer tokens, store only token digests, restrict environment access to the service account, and grant only required permissions.

Risk: Consensus results can be mistaken for automatic action execution or a durable decision ledger.

Mitigation: Treat output as a checksum-backed evaluation result; downstream systems should handle idempotent execution and preserve evidence when durable records are required.

Risk: Signed statements establish issuer provenance, not factual truth or legal compliance.

Mitigation: Verify the underlying evidence and apply domain review before relying on a resolved assertion.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/schchit/skills/coe-consensus)
- [README.md](artifact/README.md)
- [SECURITY.md](artifact/SECURITY.md)
- [CHANGELOG.md](artifact/CHANGELOG.md)
- [manifest.json](artifact/manifest.json)

## Skill Output:

**Output Type(s):** [json, configuration, guidance]

**Output Format:** [JSON API responses with resolved status, conflicts, and optional Shared World State checksum.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts up to 128 signed events per request; the Shared World State hash is an integrity checksum, not a signed tamper-proof record.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
