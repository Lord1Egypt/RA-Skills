## Description:

Archon Keymaster is a DID toolkit for managing identities, verifiable credentials, encrypted messaging, Nostr keys, file encryption/signing, aliases, challenge/response authorization, groups, assets, and cryptographic polls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[macterra](https://clawhub.ai/user/macterra)

### License/Terms of Use:


## Use Case:

Developers, engineers, and agent operators use this skill to create and manage decentralized identities, issue or accept credentials, exchange encrypted messages, sign or encrypt files, derive Nostr keys, manage DID groups and assets, and run cryptographic polls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles wallet passphrases, mnemonics, and derived Nostr private keys that could be exposed through files, logs, or agent transcripts.

Mitigation: Use a test wallet first, keep ARCHON_PASSPHRASE out of shared transcripts, restrict secret files to owner-only permissions, and treat mnemonic or nsec output as highly sensitive.

Risk: The artifact includes remote or dependency execution patterns such as npx package execution, npm dependency installation, and a documented curl-to-shell installer.

Mitigation: Avoid curl | sh, install and pin dependencies separately, review scripts before execution, and load sensitive environment variables only after dependencies are installed.

Risk: The default gatekeeper configuration can send encrypted DID data over public network services.

Mitigation: Verify the configured ARCHON_GATEKEEPER_URL, use a local gatekeeper for sensitive testing when appropriate, and confirm recipient DIDs before encryption or messaging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/macterra/skills/archon-keymaster)
- [Archon documentation](https://github.com/archetech/archon)
- [Keymaster reference](https://github.com/archetech/archon/tree/main/keymaster)
- [W3C DID specification](https://www.w3.org/TR/did-core/)
- [W3C Verifiable Credentials](https://www.w3.org/TR/vc-data-model/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands, JSON examples, and generated local files or command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local shell scripts and environment variables for wallet, passphrase, and gatekeeper configuration.]

## Skill Version(s):

0.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
