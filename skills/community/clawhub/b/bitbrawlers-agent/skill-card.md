## Description:

Billions decentralized identity for agents. Link agents to human identities using Billions ERC-8004 and Attestation Registries. Verify and generate authentication proofs. Based on iden3 self-sovereign identity protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohammadhabibulloh](https://clawhub.ai/user/mohammadhabibulloh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create and manage decentralized agent identities, link an agent DID to a human owner, sign authentication challenges, and verify identity ownership proofs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles long-lived private keys and can store them unencrypted on disk if encryption is not configured.

Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before creating or importing identities and restrict access to $HOME/.openclaw/billions.

Risk: Generated signed tokens and pairing links are sensitive authentication material.

Mitigation: Share tokens and pairing links only with the intended verifier and avoid logging or reusing them.

Risk: The security review guidance calls for review of the unexpected agent.json mismatch and dependency posture before important authentication use.

Mitigation: Confirm the release metadata, agent identity description, and dependency set before relying on the skill for important authentication flows.

Risk: Manual cryptographic workarounds or direct edits to stored identity files can undermine identity integrity.

Mitigation: Use the provided scripts, stop on non-zero script exits, and do not manually manipulate files under $HOME/.openclaw/billions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mohammadhabibulloh/skills/bitbrawlers-agent)
- [Billions Network](https://billions.network/)
- [OpenClaw Environment Documentation](https://docs.openclaw.ai/help/environment)
- [README.md](README.md)
- [SKILL.md](SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Text, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and script outputs as JSON, plain text status messages, DID strings, or verification URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and can use BILLIONS_NETWORK_MASTER_KMS_KEY to encrypt stored private keys.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
