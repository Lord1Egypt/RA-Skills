## Description: <br>
Core Archon DID toolkit - identity management, verifiable credentials, encrypted messaging (dmail), Nostr integration, file encryption/signing, aliasing, authorization (challenge/response), groups, and cryptographic polls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[macterra](https://clawhub.ai/user/macterra) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and agent operators use this skill to create and manage Archon DIDs, issue and accept verifiable credentials, send encrypted DID messages, sign or encrypt files, derive Nostr keys, manage aliases and groups, and run cryptographic polls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill manages long-lived DID wallet secrets, including wallet files, passphrases, mnemonics, and Nostr secret keys. <br>
Mitigation: Use it only in trusted workspaces, keep ~/.archon.env and wallet files permission-restricted, avoid exposing terminal logs, and store recovery mnemonics offline. <br>
Risk: The documentation includes an unpinned curl-to-shell installer path for the Nostr nak tool. <br>
Mitigation: Independently review and verify the installer or install nak through a trusted pinned package source before running Nostr workflows. <br>
Risk: Misconfigured environment variables or gatekeeper endpoints can affect wallet access and network operations. <br>
Mitigation: Review ARCHON_WALLET_PATH, ARCHON_PASSPHRASE, and ARCHON_GATEKEEPER_URL before execution and use separate test identities for evaluation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/macterra/archon-keymaster) <br>
- [Archon project](https://github.com/archetech/archon) <br>
- [Keymaster CLI reference](https://github.com/archetech/archon/tree/main/keymaster) <br>
- [W3C DID Core](https://www.w3.org/TR/did-core/) <br>
- [W3C Verifiable Credentials context](https://www.w3.org/ns/credentials/v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON examples, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute local shell scripts that invoke Node.js/npx, read wallet environment variables, and produce DIDs, credentials, encrypted messages, signatures, or local output files.] <br>

## Skill Version(s): <br>
0.1.4 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
