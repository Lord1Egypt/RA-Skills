## Description: <br>
Deploy smart contracts, bridge assets, trade tokens, place Myriad prediction market actions, check balances, transfer assets, and interact with Abstract mainnet using Abstract-focused scripts and references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Masoncags-tech](https://clawhub.ai/user/Masoncags-tech) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to operate on Abstract mainnet and testnet, including wallet setup, contract deployment, token transfers, bridging, DEX swaps, balance checks, event monitoring, and Myriad prediction market actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate blockchain transactions that move real funds. <br>
Mitigation: Use a dedicated low-balance wallet and verify every recipient, spender, contract, route, chain, market, and amount before execution. <br>
Risk: Private keys may be exposed if pasted into shared shells, command history, or logs. <br>
Mitigation: Avoid using primary wallet keys and keep private keys out of shared terminals, logs, and transcripts. <br>
Risk: Full-balance bridge or zero-minimum-output swap behavior can cause unintended losses. <br>
Mitigation: Avoid those scripts with meaningful funds and set conservative amounts and minimum outputs before running transactions. <br>


## Reference(s): <br>
- [Abstract Contract Addresses](references/addresses.md) <br>
- [Abstract Global Wallet Guide](references/agw.md) <br>
- [Abstract DEX Reference](references/dex.md) <br>
- [Myriad Prediction Markets on Abstract](references/myriad.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Hardhat Abstract Configuration](references/hardhat.config.js) <br>
- [Abstract Docs](https://docs.abs.xyz) <br>
- [Abstract Global Wallet Docs](https://docs.abs.xyz/abstract-global-wallet/overview) <br>
- [Abstract Explorer](https://abscan.org) <br>
- [Relay Abstract Bridge](https://relay.link/bridge/abstract) <br>
- [Myriad API](https://api-v2.myriadprotocol.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include transaction, contract, wallet, bridge, DEX, and prediction market parameters that require human verification before execution.] <br>

## Skill Version(s): <br>
1.6.0 (source: frontmatter and server-resolved release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
