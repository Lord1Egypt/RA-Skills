## Description: <br>
Clawlett enables Base Mainnet token swaps and Trenches token creation or trading through a Gnosis Safe constrained by Zodiac Roles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xArdi](https://clawhub.ai/user/0xArdi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Clawlett to initialize a purpose-limited Safe, preview Base Mainnet swaps, and execute confirmed swaps or Trenches token actions. It is intended for wallet-trading workflows where token addresses, fees, permissions, and on-chain execution are reviewed before action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real-money on-chain actions can execute when swap, create, buy, or sell commands are run with execution intent. <br>
Mitigation: Use quote or preview mode by default, require explicit user confirmation before execution, and verify fees, token addresses, contract addresses, and Zodiac Roles permissions before running execution commands. <br>
Risk: Local wallet and session files such as config/agent.pk and wallet.json grant powerful access to the configured Safe workflow. <br>
Mitigation: Protect the config directory like wallet secrets, restrict filesystem access, avoid sharing or committing these files, and use a small purpose-limited Safe. <br>
Risk: Unverified or impersonating tokens can lead to unintended trades or loss of funds. <br>
Mitigation: Prefer verified Base Mainnet token addresses, display contract address, volume, and liquidity for unverified tokens, and require confirmation before proceeding. <br>
Risk: Trenches create, buy, and sell commands may cause immediate token-market actions. <br>
Mitigation: Do not run Trenches create, buy, or sell commands unless the user intends immediate on-chain action and has reviewed all token parameters. <br>


## Reference(s): <br>
- [Clawlett ClawHub Page](https://clawhub.ai/0xArdi/clawlett) <br>
- [Skill Documentation](artifact/SKILL.md) <br>
- [Migration Guide](artifact/MIGRATION_GUIDE.md) <br>
- [Safe Transaction Builder](https://app.safe.global) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce quote summaries, local wallet configuration, transaction hashes, and migration steps for Base Mainnet workflows.] <br>

## Skill Version(s): <br>
0.4.1 (source: server release metadata and release changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
