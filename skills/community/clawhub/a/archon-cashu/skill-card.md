## Description:

Archon Cashu helps agents manage Cashu ecash wallets, send and receive sats, and create Archon DID-based P2PK-locked tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[macterra](https://clawhub.ai/user/macterra)

### License/Terms of Use:


## Use Case:

Developers and operators who use Archon DID identities and Cashu wallets use this skill to configure wallets, mint or receive sats, send DID-locked ecash, and manage wallet backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet backups can expose sensitive wallet material if backup data is uploaded before local encryption is fixed.

Mitigation: Do not run backup.sh with real wallet data until local encryption before IPFS upload is implemented and verified.

Risk: Unpinned npx workflows can execute changing remote package code.

Mitigation: Pin dependency versions, review packages before use, and run the workflows in an isolated environment when funds or wallet keys are involved.

Risk: LNbits auto-pay can spend funds without strong user confirmation or invoice validation.

Mitigation: Use manual invoice payment for real funds until explicit confirmations and validation are added to the payment path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/macterra/skills/archon-cashu)
- [Nutshell Cashu CLI](https://github.com/cashubtc/nutshell)
- [Archon project](https://github.com/ArcHive-tech/archon)
- [LNbits](https://lnbits.com)
- [npub.cash LNURL endpoint](https://npub.cash/.well-known/lnurlp/$NPUB)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include DIDs, sat amounts, Cashu tokens, wallet paths, and environment variable names.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
