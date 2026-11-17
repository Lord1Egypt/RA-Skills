## Description:

Leanjutsu helps agents create and manage Billions Network decentralized identities, link them to human owners, and generate or verify authentication proofs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kondifun](https://clawhub.ai/user/kondifun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create and manage agent DIDs, link agents to human identities, sign challenges, and verify identity ownership.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill manages DID private keys and authentication proofs with unsafe defaults.

Mitigation: Review before installing, set BILLIONS_NETWORK_MASTER_KMS_KEY before creating or importing identities, and restrict $HOME/.openclaw/billions to the current user.

Risk: Passing a private key with --key can expose it through shell history or logs.

Mitigation: Avoid passing private keys on the command line; prefer generating a new identity after configuring encrypted key storage.

Risk: Signed challenge tokens can authenticate identity ownership if shared beyond the intended verifier.

Mitigation: Treat signed challenge tokens as sensitive and share them only with the expected verification flow.

Risk: The scanner recommends stronger defaults for encrypted storage, file permissions, challenge lifetime, and install pinning.

Mitigation: Prefer a version that enforces encrypted key storage, restrictive permissions, single-use expiring challenges, and pinned install instructions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kondifun/skills/artefact-144794444)
- [Billions Network](https://billions.network/)
- [OpenClaw Environment Documentation](https://docs.openclaw.ai/help/environment)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; runtime scripts return DID strings, JSON responses, and verification links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=20 and npm; identity data is stored under $HOME/.openclaw/billions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
