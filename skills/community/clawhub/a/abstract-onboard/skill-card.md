## Description:

Deploy smart contracts, bridge assets, trade tokens, place Myriad predictions, check balances, transfer assets, and interact with Abstract mainnet on Abstract (ZK Stack L2).

This skill is ready for commercial/non-commercial use.

## Publisher:

[masoncags-tech](https://clawhub.ai/user/masoncags-tech)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to prepare and run Abstract blockchain operations, including wallet setup, contract deployment, bridging, DEX swaps, prediction market trades, balance checks, and contract reads or writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can sign irreversible mainnet transactions.

Mitigation: Use a dedicated low-balance wallet first and manually verify every recipient, contract, chain, amount, and transaction before using real funds.

Risk: Token approvals can persist after swaps or prediction-market trades.

Mitigation: Verify each spender and allowance before approval, prefer limited approvals, and revoke allowances after use.

Risk: Relay bridge flows and arbitrary contract-write commands can move funds or call unreviewed contracts.

Mitigation: Avoid Relay and arbitrary contract-write paths unless reviewed; verify routers, spenders, ABI files, and destination addresses independently.

Risk: Dependency or SDK version drift can change wallet or transaction behavior.

Mitigation: Pin and audit dependencies, then verify derived wallet addresses and deployed bytecode before sending assets.

## Reference(s):

- [Abstract Contract Addresses](references/addresses.md)
- [Abstract Global Wallet (AGW)](references/agw.md)
- [Abstract DEX Reference](references/dex.md)
- [Hardhat config for Abstract](references/hardhat.config.js)
- [Myriad Prediction Markets on Abstract](references/myriad.md)
- [Abstract/zkSync Troubleshooting Guide](references/troubleshooting.md)
- [Abstract Docs](https://docs.abs.xyz)
- [Abstract Global Wallet Docs](https://docs.abs.xyz/abstract-global-wallet/overview)
- [Abstract Explorer](https://abscan.org)
- [Relay Abstract Bridge](https://relay.link/bridge/abstract)
- [Myriad API Docs](https://help.myriad.markets/developer-docs-v2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline JavaScript and bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run commands that sign blockchain transactions when wallet credentials are configured.]

## Skill Version(s):

1.6.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
