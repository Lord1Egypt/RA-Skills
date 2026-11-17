## Description:

Cryptographic memory for AI agents with QSEAL tamper-evidence, zero-config demo mode, and scroll-native YAML storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdvegas21](https://clawhub.ai/user/sdvegas21)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use ClawSeal to give agents persistent local memory for preferences, facts, insights, and decisions, with QSEAL signature checks intended to detect memory tampering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run a persistent local memory service that stores long-lived user or project information.

Mitigation: Install only after reviewing the service behavior, storage location, and retention expectations; use it only for information appropriate for local persistence.

Risk: The security summary reports weak access controls for the local service.

Mitigation: Keep the service bound to local use, avoid exposing it on untrusted networks, and prefer a release with authentication before broader deployment.

Risk: The security summary reports unreliable integrity verification.

Mitigation: Treat QSEAL verification results as tamper-evidence that needs review, and prefer a release with corrected verification behavior for sensitive workflows.

Risk: The install flow registers an auto-starting service and uses unpinned dependency ranges.

Mitigation: Require opt-in service registration, review dependency versions before installation, and pin dependencies in controlled environments.

## Reference(s):

- [ClawSeal ClawHub Skill Page](https://clawhub.ai/sdvegas21/skills/clawseal)
- [ClawSeal GitHub Project](https://github.com/mvar-security/ClawSeal)
- [ClawSeal PyPI Package](https://pypi.org/project/clawseal/)
- [OpenClaw Integration Guide](OPENCLAW_INTEGRATION.md)
- [Demo Conversation](demo_conversation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with curl commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local service setup guidance and memory operation examples for remember, recall, verify, and health-check workflows.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
