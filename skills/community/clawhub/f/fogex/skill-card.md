## Description: <br>
ForgeX helps an agent provide command-line guidance for Solana wallet management, token launches, batch trading, transfers, and on-chain market-making workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leo-cells-156](https://clawhub.ai/user/leo-cells-156) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent explain ForgeX CLI setup and commands for Solana wallet groups, token creation, transfers, trading, and market-making operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs users toward wallet control and private-key handling. <br>
Mitigation: Use isolated test wallets with small balances, avoid valuable private-key imports, do not paste real private keys or passwords into shell commands, and protect exported backups. <br>
Risk: The skill can guide live transfers, trades, token launches, sniping, daemons, and other on-chain operations. <br>
Mitigation: Run supported commands with dry-run simulation first and require explicit human review before any live transfer, trade, token launch, daemon, sniping, or other irreversible on-chain action. <br>
Risk: The security summary flags automated trading and volume or price manipulation workflows with limited safety guidance. <br>
Mitigation: Independently verify the npm package and publisher, review intended market impact before use, and avoid deploying workflows that could create misleading volume or price movement. <br>


## Reference(s): <br>
- [ForgeX ClawHub Skill Page](https://clawhub.ai/leo-cells-156/fogex) <br>
- [forgex-cli npm Package](https://www.npmjs.com/package/forgex-cli) <br>
- [Solana](https://solana.com) <br>
- [Jito](https://jito.wtf) <br>
- [Pump.fun](https://pump.fun) <br>
- [Sonic SVM](https://sonic.game) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dry-run recommendations, command options, and wallet or trading workflow steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
