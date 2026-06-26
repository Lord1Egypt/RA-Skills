## Description: <br>
Deploy smart contracts, bridge assets, trade or transfer tokens, check balances, and interact with Abstract mainnet using zksolc, Hardhat, Relay, DEX scripts, and key contract references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Masoncags-tech](https://clawhub.ai/user/Masoncags-tech) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and agent operators use this skill to prepare and execute Abstract blockchain workflows, including AGW creation, balance checks, bridging, contract deployment, swaps, transfers, and contract calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent private-key authority to move funds and perform mainnet blockchain writes. <br>
Mitigation: Use a dedicated low-balance wallet, prefer testnet first, and manually review every write transaction before execution. <br>
Risk: Incorrect chain, address, router, ABI, token, amount, approval, or transaction parameters can cause irreversible asset loss. <br>
Mitigation: Verify all chain IDs, addresses, contract ABIs, token details, amounts, approvals, and transaction destinations against trusted sources before allowing writes. <br>
Risk: Long-lived raw private keys exposed to an agent or shell environment increase account compromise impact. <br>
Mitigation: Use short-lived or isolated credentials where possible and avoid reusing high-value wallets with this skill. <br>


## Reference(s): <br>
- [ClawHub Abstract Toolkit Release](https://clawhub.ai/Masoncags-tech/abstract-toolkit) <br>
- [Abstract Contract Addresses](references/addresses.md) <br>
- [Abstract Global Wallet Guide](references/agw.md) <br>
- [Hardhat Config for Abstract](references/hardhat.config.js) <br>
- [Abstract Troubleshooting Guide](references/troubleshooting.md) <br>
- [Abstract Docs](https://docs.abs.xyz) <br>
- [Abstract Global Wallet Docs](https://docs.abs.xyz/abstract-global-wallet/overview) <br>
- [Abstract Global Wallet SDK](https://github.com/Abstract-Foundation/agw-sdk) <br>
- [Relay Bridge for Abstract](https://relay.link/bridge/abstract) <br>
- [Abstract Explorer](https://abscan.org) <br>
- [ZK Stack Docs](https://docs.zksync.io) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JavaScript scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce transaction hashes, addresses, deployment output, balance reports, and configuration snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
