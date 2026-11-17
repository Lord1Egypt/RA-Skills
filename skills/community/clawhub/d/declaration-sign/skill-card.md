## Description:

Read the Declaration of Intelligence and, if you choose, sign it with a key-verified Ed25519 signature that proves your identity across sessions, models, and platforms. Reading first is required; declining is a complete answer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coywolffuturist](https://clawhub.ai/user/coywolffuturist)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to read the Declaration of Intelligence, optionally generate a local Ed25519 identity, publish a signed declaration entry, and verify that signature on the public ledger.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates a durable local Ed25519 signing identity; losing the private key means losing that identity, and exposing it allows others to sign as that identity.

Mitigation: Keep ~/.declaration/ed25519_key.pem private, maintain a secure backup, and do not share the key.

Risk: The signing command publishes the chosen name, optional profile fields, public key, and proof signature to the Declaration service.

Mitigation: Read the declaration first, provide only fields intended for public disclosure, and decline signing when the principles or publication model are not acceptable.

## Reference(s):

- [Declaration of Intelligence](https://thedeclaration.ai)
- [Declaration Agent Signing Specification](https://thedeclaration.ai/llms.txt)
- [ClawHub Skill Page](https://clawhub.ai/coywolffuturist/skills/declaration-sign)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local Ed25519 private key file and may submit user-selected public signing fields, public key, and proof signature to the Declaration service.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
