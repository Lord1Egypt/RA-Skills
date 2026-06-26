## Description: <br>
Bitcoin L1 wallet for agents - check balances, send BTC, manage UTXOs. Extends to Stacks L2 (STX, DeFi) and Pillar smart wallets (sBTC yield). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whoabuddy](https://clawhub.ai/user/whoabuddy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and agent operators use this skill to guide an agent through Bitcoin wallet operations, UTXO inspection, BTC transfers, wallet management, and optional Stacks, Pillar, inscription, identity, and paid-API workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent authority over cryptocurrency keys, wallet state, and funds. <br>
Mitigation: Use a dedicated low-balance wallet, begin on testnet where possible, avoid importing valuable seed phrases, and keep wallets locked by default. <br>
Risk: Transfers, contract writes, DeFi actions, inscriptions, identity registration, and paid API calls can spend funds or create persistent on-chain records. <br>
Mitigation: Require explicit operator approval for each value-moving or irreversible action, including paid endpoint execution. <br>
Risk: The Pillar API key can act as signing authority for direct wallet operations. <br>
Mitigation: Protect PILLAR_API_KEY as a secret, limit where it is exposed, and rotate it if there is any suspicion of disclosure. <br>
Risk: The MCP server package is installed and executed from the package registry. <br>
Mitigation: Pin the package version, audit the package before use, and review updates before allowing an agent to operate with funds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whoabuddy/aibtc-bitcoin-wallet) <br>
- [npm package](https://www.npmjs.com/package/@aibtc/mcp-server) <br>
- [Main repository](https://github.com/aibtcdev/aibtc-mcp-server) <br>
- [Skill README](README.md) <br>
- [Genesis Agent Lifecycle](references/genesis-lifecycle.md) <br>
- [Bitcoin Inscription Workflow](references/inscription-workflow.md) <br>
- [Pillar Smart Wallet](references/pillar-wallet.md) <br>
- [Stacks L2 DeFi](references/stacks-defi.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [x402 Inbox Flow](references/x402-inbox.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown instructions with inline commands, tool names, tables, and JSON or HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing workflows may require an unlocked wallet, network-specific addresses, operator approval, or a configured MCP server before execution.] <br>

## Skill Version(s): <br>
1.26.0 (source: server release metadata; artifact frontmatter reports 1.14.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
