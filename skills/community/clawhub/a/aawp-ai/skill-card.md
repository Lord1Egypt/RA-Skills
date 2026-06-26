## Description: <br>
AAWP is an AI agent wallet skill for EVM chains and Solana that supports wallet lifecycle operations, transfers, swaps, bridging, DCA, price alerts, limit orders, NFTs, staking, portfolio tracking, transaction history, and DeFi actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wfce](https://clawhub.ai/user/wfce) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let an AI agent manage an on-chain wallet, inspect balances and history, prepare or execute token transfers, swaps, bridge transactions, DCA strategies, alerts, NFT actions, staking, and DeFi operations across supported EVM chains and Solana. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can grant an AI agent real wallet-signing authority over crypto assets. <br>
Mitigation: Use an isolated machine or account, begin on testnet or with tiny funds, and install only when this authority is intended. <br>
Risk: The skill includes persistent daemon, key-handling, and autonomous transaction behavior. <br>
Mitigation: Review and constrain daemon operation, key handling, bootstrap verification, and cron behavior before unattended mainnet use. <br>
Risk: Backup and restore operations can affect wallet recovery material and host files. <br>
Mitigation: Avoid restoring untrusted backups and keep recovery material offline, encrypted, and out of chats, logs, and public repositories. <br>
Risk: The release has no server-resolved import provenance for this version. <br>
Mitigation: Inspect the native binary source/provenance and verify bootstrap and binary approval behavior before relying on the skill with funds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wfce/aawp-ai) <br>
- [AAWP website](https://aawp.ai) <br>
- [Publisher profile](https://clawhub.ai/user/wfce) <br>
- [Base factory contract](https://basescan.org/address/0xAAAA3Df87F112c743BbC57c4de1700C72eB7aaAA) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and command-output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe wallet status, balances, transaction previews, setup steps, and risk-aware operating guidance.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
