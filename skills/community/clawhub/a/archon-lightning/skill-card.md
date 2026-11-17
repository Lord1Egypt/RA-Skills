## Description:

Lightning Network payments via Archon DIDs - create wallets, send/receive sats, verify payments, Lightning Address zaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[macterra](https://clawhub.ai/user/macterra)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to manage DID-linked Lightning wallets, generate and pay BOLT11 invoices, send Lightning Address zaps, verify settlement, inspect balances and history, and publish or remove Lightning endpoints in DID documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill loads wallet secrets and payment authority from the local Archon environment.

Mitigation: Install only where that access is intended, restrict `~/.archon.env` permissions, and start with very small amounts before using real funds.

Risk: The wrapper scripts invoke `npx @didcid/keymaster`, which can download or run package code at payment time if the package is not pinned or locally installed.

Mitigation: Pin or locally install a reviewed `@didcid/keymaster` version and avoid runtime package downloads during payment operations.

Risk: Publishing a Lightning endpoint to a DID can make payment metadata publicly discoverable.

Mitigation: Publish endpoints deliberately and remove them when public discoverability is no longer desired.

Risk: Lightning payments can fail, time out, remain pending, or be misinterpreted if settlement is not verified.

Mitigation: Decode invoices before payment, verify settlement after payment, and rely on wrapper commands that return failure when payment confirmation is not observed.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/macterra/skills/archon-lightning)
- [Archon Documentation](https://github.com/archetech/archon)
- [Keymaster Reference](https://github.com/archetech/archon/tree/main/keymaster)
- [Lightning Network](https://lightning.network)
- [BOLT Specifications](https://github.com/lightning/bolts)
- [Lightning Address](https://lightningaddress.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, npx, jq, ARCHON_WALLET_PATH, ARCHON_PASSPHRASE, and ARCHON_GATEKEEPER_URL.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
