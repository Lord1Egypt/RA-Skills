## Description:

Billions decentralized identity for agents. Link agents to human identities using Billions ERC-8004 and Attestation Registries. Verify and generate authentication proofs. Based on iden3 self-sovereign identity protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kondifun](https://clawhub.ai/user/kondifun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create and manage decentralized identities for agents, link an agent DID to a human owner, sign identity challenges, and verify DID ownership.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles long-lived DID private keys and may store them under $HOME/.openclaw/billions.

Mitigation: Set a high-entropy BILLIONS_NETWORK_MASTER_KMS_KEY before creating or importing identities, protect the storage directory, and review key-handling behavior before installation.

Risk: Existing private keys can be supplied on the command line.

Mitigation: Avoid passing existing private keys as CLI arguments; prefer generating a new identity in a controlled environment or use safer secret handling outside shell history.

Risk: Signing and human-agent linking actions can create identity proofs or verification links.

Mitigation: Require explicit human confirmation before running signing or linking commands and inspect the challenge content before approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kondifun/skills/artefact-144794446)
- [Billions Network](https://billions.network/)
- [OpenClaw environment documentation](https://docs.openclaw.ai/help/environment)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may create local DID, key, challenge, credential, and identity files under $HOME/.openclaw/billions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
