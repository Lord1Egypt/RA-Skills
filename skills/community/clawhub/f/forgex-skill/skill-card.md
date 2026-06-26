## Description: <br>
ForgeX CLI guides an agent through installing and using a command-line tool for Solana wallet management, token launches, batch trades, market-making workflows, and on-chain data queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[catlina-2b](https://clawhub.ai/user/catlina-2b) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to produce ForgeX CLI commands and workflow guidance for Solana wallet groups, token operations, transfers, trading, and market-making tasks. Users should treat the guidance as high-risk because it can involve private keys, real funds, and automated trading behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide users through installing an external CLI and executing crypto wallet, private-key, fund-transfer, and automated trading workflows. <br>
Mitigation: Verify the npm package and maintainer independently, review commands before execution, start with throwaway wallets and tiny test amounts, and use dry-run options before any live transaction. <br>
Risk: Commands may expose sensitive values such as passwords or private keys if entered directly on the command line or stored insecurely. <br>
Mitigation: Avoid passing secrets directly as command-line arguments where possible, use secure secret handling, and store wallet backups encrypted. <br>
Risk: Volume or price-moving workflows can misrepresent market activity or violate platform, legal, or policy rules. <br>
Mitigation: Use the skill only for lawful, compliant activity and do not use automated market-making features to create deceptive volume or manipulate prices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/catlina-2b/forgex-skill) <br>
- [npm package: forgex-cli](https://www.npmjs.com/package/forgex-cli) <br>
- [Solana](https://solana.com) <br>
- [Sonic SVM](https://sonic.game) <br>
- [Pump.fun](https://pump.fun) <br>
- [Raydium](https://raydium.io) <br>
- [Jito](https://jito.wtf) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with CLI command examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that install external packages, configure RPC endpoints, manage wallets, move funds, launch tokens, or run automated trading workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
