## Description:

ForgeX CLI helps agents guide Solana token launch, trading, market-making, wallet management, and fund-transfer workflows through a command-line tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catlina-2b](https://clawhub.ai/user/catlina-2b)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent users can use this skill to install and operate forgex-cli for Solana token creation, bundled trading, wallet group management, and fund transfers. It is intended for command guidance around on-chain workflows that may move funds or handle wallet secrets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to install and run an unaudited third-party CLI package.

Mitigation: Verify the exact forgex-cli package version and source before installation, and install it only in environments where the package publisher is trusted.

Risk: Commands may require passwords, private keys, wallet backups, or wallet CSV files.

Mitigation: Do not paste real secrets into agent chats or shell history; avoid plaintext wallet exports and keep encrypted backups outside cloud sync and source control.

Risk: The documented workflows can execute on-chain trades, token launches, and fund transfers.

Mitigation: Use dry-run modes first, review generated commands before execution, and test with low-value wallets before moving meaningful funds.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/catlina-2b/skills/forgex-cli)
- [forgex-cli npm package](https://www.npmjs.com/package/forgex-cli)
- [Solana](https://solana.com)
- [Sonic SVM](https://sonic.game)
- [Pump.fun](https://pump.fun)
- [Jito](https://jito.wtf)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and CLI option tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that install and execute third-party CLI software and interact with wallet secrets or on-chain funds.]

## Skill Version(s):

1.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
