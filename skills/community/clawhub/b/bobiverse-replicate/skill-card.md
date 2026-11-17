## Description:

Create a new Bob agent only on explicit operator command using a guarded replication runner for purposeful Bobiverse-style replication in OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theamericanmaker](https://clawhub.ai/user/theamericanmaker)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw operators use this skill to create a mission-scoped peer Bob agent from an existing workspace after explicit approval. It is intended for controlled multi-agent workspace setup, personality variation, and lineage tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can copy an entire OpenClaw workspace into a persistent peer agent.

Mitigation: Use it only from a clean or dedicated workspace, remove secrets and unrelated project data first, and review the dry-run output before approving execution.

Risk: The security evidence notes that approval-token enforcement is not guaranteed outside the invoking agent.

Mitigation: Avoid exposing shell execution to untrusted prompts, keep the operator in the loop, and execute only after an explicit command, purpose statement, and nonce-backed confirmation.

Risk: Replication can increase local agent count and persistent state.

Mitigation: Respect the documented one-clone-at-a-time flow, resource warning threshold, audit log, and default 24-hour cadence unless the operator explicitly records an override reason.

## Reference(s):

- [Bobiverse Replicate on ClawHub](https://clawhub.ai/theamericanmaker/skills/bobiverse-replicate)
- [OpenClaw](https://openclaw.ai)
- [Project Homepage](https://github.com/TheAmericanMaker/bobiverse-openclaw)
- [Security Model](SECURITY.md)
- [Architecture](ARCHITECTURE.md)
- [Serial Number Spec](SERIAL-NUMBER-SPEC.md)
- [Bobiverse Primer](docs/bobiverse-primer.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and local workspace file updates performed through the guarded runner]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw, python3, an explicit replication request, a concrete purpose statement, dry-run review, and nonce-backed confirmation before execution.]

## Skill Version(s):

1.2.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
