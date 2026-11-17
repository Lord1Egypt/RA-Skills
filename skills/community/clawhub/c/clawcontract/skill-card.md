## Description:

ClawContract is an AI-powered smart contract generator, analyzer, and deployer for BNB Chain (BSC/opBNB) that can generate Solidity, analyze security, compile, deploy, verify, interact with contracts, and run a full generate-analyze-deploy-verify pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sufnoobzac](https://clawhub.ai/user/sufnoobzac)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to generate, analyze, deploy, verify, and interact with Solidity smart contracts on BNB Smart Chain and opBNB. It is suited for agent-assisted CLI workflows that need contract source generation, security review, deployment metadata, and scanner verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation path uses an unpinned npm CLI that can access API keys and a wallet private key.

Mitigation: Install only from a trusted package source, pin or review the CLI implementation before use, and avoid storing private keys in plaintext .env files.

Risk: Deploy and state-changing interact commands can sign blockchain transactions with the configured wallet key.

Mitigation: Prefer testnet chains and throwaway low-value wallets, and require explicit human review before mainnet deployment or any state-changing interaction.

Risk: Mainnet deployment warns but does not block when a mainnet chain is selected.

Mitigation: Keep the default testnet chain for trials and require manual approval before passing bsc-mainnet or opbnb-mainnet.

Risk: Automatic AI-powered fix attempts can modify generated Solidity before deployment in the full pipeline.

Mitigation: Use --skip-fix or --skip-deploy when review is required, and inspect the final Solidity and analysis results before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sufnoobzac/skills/clawcontract)
- [ClawContract CLI Commands](references/commands.md)
- [ClawContract GitHub repository](https://github.com/cvpfus/clawcontract)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands, Solidity source files, and JSON deployment metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated contracts are written under contracts/ and deployment records under .deployments/ during normal CLI operation.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
