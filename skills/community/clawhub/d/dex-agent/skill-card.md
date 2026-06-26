## Description: <br>
DEX Agent executes Base-chain token swaps through Uniswap V3 and supports price checks, quotes, stop-loss, take-profit, portfolio tracking, and configurable trading limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[avmw2025](https://clawhub.ai/user/avmw2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to check Base-chain token prices, generate a trading wallet, quote or execute swaps, and manage stop-loss and take-profit workflows from a Python CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles real funds and the server security summary reports under-disclosed financial risk. <br>
Mitigation: Review before installing, test with tiny amounts, and use only a fresh low-balance wallet. <br>
Risk: The server security summary reports plaintext private-key storage on disk. <br>
Mitigation: Assume the private key is recoverable from local storage; do not reuse a valuable wallet and protect or delete generated wallet files after testing. <br>
Risk: The monitor command can execute automatic live sell transactions against funded positions. <br>
Mitigation: Do not run the monitor against funded positions unless automatic sales are intended and the configured stop-loss/take-profit orders have been reviewed. <br>
Risk: Swap approvals and router interactions may leave token allowances active. <br>
Mitigation: Revoke router approvals when testing or trading is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/avmw2025/dex-agent) <br>
- [Artifact skill documentation](SKILL.md) <br>
- [Artifact scripts README](scripts/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, JSON, Blockchain transactions] <br>
**Output Format:** [CLI text output, JSON wallet/order/configuration files, and signed Base-chain transaction submissions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can execute live swaps and automated sell orders when invoked with a funded wallet.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
