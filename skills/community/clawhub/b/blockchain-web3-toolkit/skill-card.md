## Description: <br>
Comprehensive blockchain toolkit for Ethereum wallet management, smart contract interaction, NFT minting, token balance checks, and gas fee monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Web3 operators use this skill to create or import Ethereum wallets, check balances, deploy and call smart contracts, mint or transfer NFTs, and monitor gas fees. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The toolkit handles wallet private keys that could be exposed through prompts, generated output, logs, or unsafe storage. <br>
Mitigation: Use testnets or empty wallets first, never paste or print a real mainnet private key in agent output, and keep secrets outside the agent context. <br>
Risk: The toolkit can sign and broadcast irreversible blockchain transactions. <br>
Mitigation: Manually verify every network, contract address, function, argument, recipient, and gas cost before any transaction is sent. <br>
Risk: Dependency or RPC-provider behavior can affect transaction safety and results. <br>
Mitigation: Pin and review dependencies, use trusted RPC/API keys, and test flows on a non-production network before using funded wallets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaiyuelv/blockchain-web3-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python and bash snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require wallet private keys, RPC/API keys, Ethereum network names, contract addresses, function arguments, and gas settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
