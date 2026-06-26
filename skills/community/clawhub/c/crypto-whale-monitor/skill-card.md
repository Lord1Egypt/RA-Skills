## Description: <br>
Monitors large cryptocurrency wallet balances on-chain using Web3 RPC to detect potential market-moving activity and can read wallet addresses from references/wallets.md or command-line input. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waleolapo](https://clawhub.ai/user/waleolapo) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers, analysts, and operators use this skill to monitor configured Ethereum wallet addresses and review balance alerts for large-holder activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Monitored wallet addresses are sent to the configured Ethereum RPC provider. <br>
Mitigation: Use a trusted RPC provider and monitor only wallet addresses you are comfortable sharing with that provider. <br>
Risk: RPC_URL may contain a provider API key or other sensitive endpoint value. <br>
Mitigation: Treat RPC_URL as sensitive configuration and use a limited-purpose provider key where possible. <br>
Risk: Scheduled execution can create ongoing background monitoring. <br>
Mitigation: Create a cron job only when continuous monitoring is intended, and document or disable the schedule when it is no longer needed. <br>


## Reference(s): <br>
- [Known Whale Wallet Addresses](references/wallets.md) <br>
- [Default Ethereum RPC endpoint](https://eth.llamarpc.com) <br>
- [ClawHub skill page](https://clawhub.ai/waleolapo/crypto-whale-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Console text output with wallet addresses, ETH balances, and threshold alerts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads wallet addresses from arguments or references/wallets.md and uses RPC_URL when configured.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
