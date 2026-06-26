## Description: <br>
Provides OpenClaw guidance and TypeScript examples for integrating Cetus Protocol SDK v2 modules on Sui. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[k66inthesky](https://clawhub.ai/user/k66inthesky) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers building Sui DeFi applications use this skill to reference Cetus SDK v2 packages, initialization patterns, and transaction-building examples across liquidity, swaps, vaults, farms, limit orders, DCA, zap, and aggregation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transaction examples can create real financial activity on Sui if run against mainnet. <br>
Mitigation: Use testnet first and verify the network, token amounts, pool or position IDs, slippage, recipients, and contract addresses before approving any transaction. <br>
Risk: Wallet-signing examples may expose users to unintended approvals or private key handling. <br>
Mitigation: Never provide a private key or approve signing unless the exact transaction and signing context are understood. <br>
Risk: Unpinned SDK package versions can change behavior over time. <br>
Mitigation: Pin package versions where possible when adapting examples into applications. <br>


## Reference(s): <br>
- [Cetus ClawHub Skill Page](https://clawhub.ai/k66inthesky/cetus) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Cetus Repository Link from README](https://github.com/k66inthesky/cetus) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with TypeScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; transaction examples may require wallet, network, pool, token, and slippage parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
