## Description: <br>
Billions decentralized identity for agents links agents to human identities using Billions ERC-8004 and Attestation Registries, and supports authentication proof generation and verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mohammadhabibulloh](https://clawhub.ai/user/mohammadhabibulloh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create and manage decentralized agent identities, link those identities to human owners, sign challenges, and verify DID ownership proofs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles private identity keys and authentication material. <br>
Mitigation: Install only if the publisher and Billions identity infrastructure are trusted; use a fresh agent identity key rather than a funded wallet key. <br>
Risk: Identity keys may be stored under $HOME/.openclaw/billions and can be plaintext if encryption is not configured. <br>
Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before creating identities and restrict access to $HOME/.openclaw/billions. <br>
Risk: Private keys or long-lived tokens could be exposed through shell commands or chat transcripts. <br>
Mitigation: Avoid passing private keys or long-lived tokens directly in shell commands or chat transcripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mohammadhabibulloh/bitbrawlers-agent) <br>
- [Billions Network](https://billions.network/) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and may read or write identity data under $HOME/.openclaw/billions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
