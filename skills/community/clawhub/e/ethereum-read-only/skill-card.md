## Description: <br>
Guides agents in using Foundry cast for wallet-free, read-only Ethereum state inspection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Byron-McKeeby](https://clawhub.ai/user/Byron-McKeeby) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Web3 analysts use this skill to prepare read-only Foundry cast commands for inspecting Ethereum blocks, contract state, event logs, ENS records, ABI data, and DeFi wallet balances without wallet signing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External RPC and API providers may observe queried wallet addresses, ENS names, contracts, and transaction lookups. <br>
Mitigation: Use a dedicated low-privilege RPC key and a trusted or self-hosted node for sensitive investigations. <br>
Risk: The guide includes shell commands for installing Foundry and running networked command examples. <br>
Mitigation: Review the official installer and each command before execution, and do not enter private keys or seed phrases while using this read-only skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Byron-McKeeby/ethereum-read-only) <br>
- [Foundry installer](https://foundry.paradigm.xyz) <br>
- [Ankr Ethereum RPC endpoint](https://rpc.ankr.com/eth) <br>
- [Ankr Polygon RPC endpoint](https://rpc.ankr.com/polygon) <br>
- [4byte function signature API](https://www.4byte.directory/api/v1/signatures/?hex_signature=0x$selector) <br>
- [4byte event signature API](https://www.4byte.directory/api/v1/event-signatures/?hex_signature=0x$event_sig) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Ethereum RPC workflows; examples depend on Foundry cast, jq, curl, and configured RPC endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
