## Description:

ForgeX CLI helps agents guide users through wallet management, token launches, batch trading, and on-chain market-making workflows on Solana.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leo-cells-156](https://clawhub.ai/user/leo-cells-156)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, traders, and agent users use this skill to generate guidance and CLI commands for configuring ForgeX, managing Solana wallet groups, launching tokens, and automating batch trading workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides users through workflows involving real funds, private keys, and wallet backups.

Mitigation: Use disposable or low-value wallets until the CLI package version and source are verified; avoid pasting real passwords or private keys into shell commands; prefer encrypted backups over CSV files.

Risk: Live token-launch, transfer, and trading commands can trigger irreversible on-chain transactions.

Mitigation: Run dry-runs with strict limits first, then review wallet groups, token addresses, amounts, slippage, and daemon settings before any live execution.

Risk: The server security verdict is suspicious because examples are under-scoped for cryptocurrency wallet and trading safety.

Mitigation: Review the skill carefully before installation or use, verify the package and publisher context, and keep operational limits conservative.

## Reference(s):

- [ForgeX CLI on ClawHub](https://clawhub.ai/leo-cells-156/skills/fogex)
- [forgex-cli npm package](https://www.npmjs.com/package/forgex-cli)
- [Solana](https://solana.com)
- [Sonic SVM](https://sonic.game)
- [Pump.fun](https://pump.fun)
- [Jito](https://jito.wtf)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing guidance for ForgeX CLI workflows; the skill itself does not generate files.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
