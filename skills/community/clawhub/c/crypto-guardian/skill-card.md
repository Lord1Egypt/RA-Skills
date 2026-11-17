## Description:

Provides security guidance and checks for safely managing crypto wallets, keys, seed phrases, approvals, multisig, and incident response for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayh-25](https://clawhub.ai/user/ayh-25)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to evaluate cryptocurrency wallet operations, choose safer key-handling patterns, manage approvals, and respond to suspected key exposure or theft.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes unsafe guidance that can be read as permitting wallet recovery secrets or private keys in plaintext .env files.

Mitigation: Do not follow those examples; keep recovery phrases offline or hardware-backed, and use a hardware wallet, isolated signer, or proper secret manager with narrowly scoped runtime access.

Risk: If the .env seed phrase or raw private-key guidance was already followed, the affected wallet secret may be exposed.

Mitigation: Treat the secret as compromised, move funds to a newly generated secure wallet, and retire the old wallet secret.

## Reference(s):

- [Crypto Guardian on ClawHub](https://clawhub.ai/ayh-25/skills/crypto-guardian)
- [Base Token Approval Checker](https://basescan.org/tokenapprovalchecker)
- [Revoke.cash](https://revoke.cash/)
- [Safe Multisig App](https://app.safe.global/)
- [Ledger Phishing Guidance](https://www.ledger.com/stop-phishing-attacks)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown checklists, incident-response steps, and occasional code or shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes wallet-security checklists, key-handling guidance, approval review steps, and incident-response guidance.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
