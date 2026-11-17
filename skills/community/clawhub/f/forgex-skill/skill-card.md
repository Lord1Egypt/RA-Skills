## Description:

ForgeX CLI enables agents to guide Solana wallet management, token launches, transfers, batch trades, and on-chain market-making workflows through command-line examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catlina-2b](https://clawhub.ai/user/catlina-2b)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for ForgeX CLI setup, wallet operations, token launch, trading, transfer, and market-making command guidance. It is intended for high-risk crypto operations where dry runs and isolated test wallets should be used before live execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live ForgeX commands can sign transactions and cause irreversible fund loss.

Mitigation: Use isolated test wallets first, keep funds minimal, and run dry-run simulations before any live transaction.

Risk: Examples pass wallet passwords and private keys through command-line arguments or CSV files.

Mitigation: Avoid entering real private keys or passwords on the command line, do not create plaintext CSV wallet backups, and prefer encrypted exports for any wallet material.

Risk: The installed npm package may differ from the documented behavior.

Mitigation: Verify the npm package provenance and exact version before installation or execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/catlina-2b/skills/forgex-skill)
- [ForgeX CLI npm package](https://www.npmjs.com/package/forgex-cli)
- [Solana](https://solana.com)
- [Sonic SVM](https://sonic.game)
- [Pump.fun](https://pump.fun)
- [Raydium](https://raydium.io)
- [Jito](https://jito.wtf)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command examples may include dry-run flags, wallet parameters, RPC endpoints, token addresses, passwords, and file paths supplied by the user.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
