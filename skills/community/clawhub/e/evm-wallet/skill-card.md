## Description: <br>
Self-sovereign EVM wallet for AI agents that can create a crypto wallet, check balances, send ETH or ERC20 tokens, swap tokens, and interact with smart contracts across Base, Ethereum, Polygon, Arbitrum, and Optimism while storing private keys locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[surfer77](https://clawhub.ai/user/surfer77) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent create and operate a local self-custodied EVM wallet, inspect balances, send ETH or ERC20 tokens, swap tokens, and interact with smart contracts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs live unpinned code that can control real funds. <br>
Mitigation: Review or pin the GitHub code before installing and use a dedicated low-balance wallet. <br>
Risk: The local wallet private key can be exposed if ~/.evm-wallet.json is shared or accessed by the wrong party. <br>
Mitigation: Protect ~/.evm-wallet.json, never share its contents, and restrict direct access to the server where it is stored. <br>
Risk: Transfers, swaps, and contract writes can spend funds or perform irreversible onchain actions. <br>
Mitigation: Manually verify every recipient, chain, token, amount, gas estimate, swap quote, and contract write before allowing execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/surfer77/evm-wallet) <br>
- [Project homepage](https://github.com/surfer77/evm-wallet-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and git; wallet state is stored locally at ~/.evm-wallet.json.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
