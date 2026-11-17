## Description:

Provides guidance and TypeScript examples for using Cetus Protocol SDK v2 modules to build DeFi applications on Sui.

This skill is ready for commercial/non-commercial use.

## Publisher:

[k66inthesky](https://clawhub.ai/user/k66inthesky)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill as a reference for installing and initializing Cetus SDK v2 packages, building Sui DeFi workflows, and generating transaction payload examples for swaps, liquidity, vaults, farms, orders, and aggregation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes live on-chain transaction examples that could submit irreversible Sui transactions when used with a real keyPair.

Mitigation: Use testnet or simulation first, and review payloads, amounts, assets, slippage, and irreversibility before allowing any agent to submit a transaction.

Risk: Package and marketplace source confusion could lead users to install or trust the wrong Cetus or ClawHub package.

Mitigation: Verify Cetus SDK package sources and the ClawHub skill source before installing or using generated guidance.

Risk: The README contains unrelated development transcript and local environment details.

Mitigation: Clean the README before redistribution so public documentation contains only release-relevant user guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/k66inthesky/skills/cetus)
- [Artifact skill guide](artifact/SKILL.md)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with TypeScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reference-oriented output that includes SDK installation, initialization, utility, and transaction payload examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
