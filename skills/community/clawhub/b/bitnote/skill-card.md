## Description: <br>
BitNote provides decentralized encrypted memory for agents to store identity, secrets, messages, and critical knowledge outside centralized infrastructure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RockwellShah](https://clawhub.ai/user/RockwellShah) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and agent operators use BitNote to preserve encrypted agent identity, secrets, critical knowledge, and agent-to-agent messages with optional human oversight. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use local key material to sign and broadcast on-chain transactions. <br>
Mitigation: Keep dry-run mode as the default, require explicit human approval before non-dry-run writes, and avoid wallets or contract authorities that can move meaningful funds unless intentionally needed. <br>
Risk: Passphrases or decrypted private key material could be exposed through logs, chat output, or committed files. <br>
Mitigation: Use at least 256 bits of passphrase entropy, store passphrases in environment variables or a secret manager, keep profile files free of secrets, and redact private details in shared logs. <br>
Risk: Plaintext or incorrectly addressed encrypted content could become difficult to remove or unrecoverable after on-chain publication. <br>
Mitigation: Never store plaintext secrets on-chain, use the canonical write and share scripts, verify usernames and recipients before use, and rely on stable request ids for deterministic retries. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/RockwellShah/bitnote) <br>
- [BitNote Contracts](references/contracts.md) <br>
- [BitNote Ops Runbook](references/ops.md) <br>
- [BitNote App](https://app.bitnote.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, environment variables, and operational checks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write and share operations may require BITNOTE_PASSPHRASE, profile settings, and optional RPC or Snowtrace configuration; dry-run writes are recommended before broadcast.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
