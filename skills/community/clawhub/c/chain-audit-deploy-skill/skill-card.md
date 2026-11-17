## Description:

Audit and deploy blockchain smart contracts for Solidity, Sui Move, and Solana projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rzexin](https://clawhub.ai/user/rzexin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and smart contract engineers use this skill to audit Solidity, Sui Move, and Solana contracts, produce findings, and prepare deployment commands. It supports audit-first deployment workflows for testnet, devnet, localnet, and mainnet targets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet keys or broad secrets may be exposed during deployment workflows.

Mitigation: Use a sandboxed workspace without production wallet files or broad secrets, and avoid real private keys unless the exact command and target have been independently checked.

Risk: Installer commands that pipe remote content to a shell may run unverified code.

Mitigation: Pin and verify blockchain tooling before installation instead of copy-pasting pipe-to-shell installers.

Risk: Deployment commands can send live blockchain transactions and spend real funds.

Mitigation: Prefer dry runs and testnet or devnet targets; require explicit confirmation and independent review before mainnet use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rzexin/skills/chain-audit-deploy-skill)
- [Publisher profile](https://clawhub.ai/user/rzexin)
- [Project homepage](https://git.woa.com/jasonruan/chain-audit-deploy-skill)
- [Multi-Chain Deployment Guide](references/deployment_guide.md)
- [Solidity Audit Rules Reference](references/solidity_audit_rules.md)
- [Sui Move Audit Rules Reference](references/sui_move_audit_rules.md)
- [Solana Audit Rules Reference](references/solana_audit_rules.md)
- [Audit Report Template](assets/report_template.md)
- [Foundry installer](https://foundry.paradigm.xyz)
- [Sui CLI source](https://github.com/MystenLabs/sui.git)
- [Anchor source](https://github.com/coral-xyz/anchor)
- [Solana CLI installer](https://release.anza.xyz/stable/install)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown audit reports, JSON audit summaries, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include pass, conditional pass, or fail audit gates; deployment output can include contract addresses, transaction hashes, explorer links, and gas estimates.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
