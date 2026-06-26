## Description: <br>
ForgeX CLI helps an agent guide Solana token launches, wallet-group management, transfers, trading, and market-making workflows through command-line operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Catlina-2B](https://clawhub.ai/user/Catlina-2B) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, token operators, and agent users use this skill to install and run ForgeX commands for wallet groups, token creation, trades, transfers, and market-making workflows. Because these workflows can affect private keys and real on-chain funds, users should treat them as high-impact crypto automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent high-impact control over private keys and real on-chain funds. <br>
Mitigation: Review before installing, use isolated low-value wallets, prefer testnet and --dry-run first, and require explicit human approval before any mainnet transfer, token launch, sniping, volume bot, or price-robot action. <br>
Risk: Agent-visible commands and wallet workflows can expose private keys, passwords, or plaintext wallet backups. <br>
Mitigation: Do not paste real private keys or important passwords into agent-visible commands, avoid plaintext CSV backups, and verify the npm package and publisher independently before use. <br>
Risk: Automated trading, token-launch, and market-making commands can create irreversible transactions or financial loss. <br>
Mitigation: Start with --dry-run, small amounts, and low-value wallets; require human confirmation for any live transaction or strategy change. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/Catlina-2B/forgex-cli) <br>
- [npm package: forgex-cli](https://www.npmjs.com/package/forgex-cli) <br>
- [Solana](https://solana.com) <br>
- [Sonic SVM](https://sonic.game) <br>
- [Pump.fun](https://pump.fun) <br>
- [Jito](https://jito.wtf) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with command examples and CLI output options such as JSON, table, or minimal text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may perform live on-chain operations; many examples support --dry-run and password-protected wallet actions.] <br>

## Skill Version(s): <br>
1.0.3 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
