## Description: <br>
Bitget Wallet Skill.Disabled provides agent-facing guidance and Python commands for Bitget Wallet market data, token checks, swap workflows, wallet signing, and x402 payments, while release evidence says this version is disabled. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xunbin0908](https://clawhub.ai/user/xunbin0908) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for Bitget Wallet-related market data, token risk checks, portfolio balances, swap quotes, signing guidance, and x402 payment flows. The release changelog states this version is disabled, so users should confirm availability before attempting wallet, trading, or payment operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary says the artifact is a functional crypto wallet, trading, and payment skill with real fund-moving authority despite metadata that says it is disabled. <br>
Mitigation: Install only when intentionally using an agent-capable crypto wallet or trading helper, and verify whether the disabled release should perform any wallet, swap, or payment operation. <br>
Risk: Wallet signing, swap, and x402 payment flows can authorize real asset transfers. <br>
Mitigation: Use a fresh low-balance wallet, avoid existing seed phrases or high-value keys, and review every transaction or payment before approval. <br>
Risk: Unreviewed updates can change fund-moving behavior. <br>
Mitigation: Avoid unpinned self-updates unless the diff is reviewed before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xunbin0908/bitget-wallet-skill-disabled) <br>
- [Bitget Wallet API documentation](https://web3.bitget.com/en/docs) <br>
- [README](README.md) <br>
- [Commands reference](docs/commands.md) <br>
- [Wallet signing guide](docs/wallet-signing.md) <br>
- [Swap guide](docs/swap.md) <br>
- [Market data guide](docs/market-data.md) <br>
- [x402 payments guide](docs/x402-payments.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May involve wallet, swap, signing, and payment actions; users should review generated commands and transaction details before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
