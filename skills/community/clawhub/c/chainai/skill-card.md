## Description: <br>
Ethereum and EVM blockchain CLI skill for signing messages, sending tokens, swapping via 1inch Fusion, checking balances, broadcasting transactions, and managing wallets across Ethereum and BNB Smart Chain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kvhnuke](https://clawhub.ai/user/kvhnuke) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use ChainAI to run non-interactive Ethereum and EVM wallet, balance, signing, transaction, broadcast, and token-swap workflows from a CLI. It is intended for blockchain operations that require explicit parameter passing and careful review before any fund-moving action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI can give an agent private-key control over real blockchain funds. <br>
Mitigation: Use a dedicated low-balance wallet, keep CHAINAI_PRIVATE_KEY out of logs and persistent plaintext storage, and prefer the environment variable over command-line private-key flags. <br>
Risk: Send, swap, broadcast, and raw signing actions can be irreversible or authorize unintended on-chain activity. <br>
Mitigation: Require explicit user approval before fund-moving actions, verify addresses, networks, token contracts, and amounts manually, and use raw hash signing only when no safer signing method applies. <br>
Risk: Retrying uncertain blockchain operations can duplicate or worsen fund-moving actions. <br>
Mitigation: Check on-chain transaction or swap status before retrying any uncertain send, swap, broadcast, or signing workflow. <br>


## Reference(s): <br>
- [ClawHub ChainAI release page](https://clawhub.ai/kvhnuke/chainai) <br>
- [ChainAI homepage](https://github.com/kvhnuke/chainai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands run through npx chainai and private-key operations require CHAINAI_PRIVATE_KEY or an explicit private-key flag.] <br>

## Skill Version(s): <br>
0.0.12 (source: server release metadata; artifact frontmatter reports 0.0.10) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
