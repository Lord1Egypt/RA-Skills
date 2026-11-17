## Description:

Use when managing Crunch coordinators, competitions (crunches), rewards, checkpoints, staking, or cruncher accounts via the crunch-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philippwassibauer](https://clawhub.ai/user/philippwassibauer)

### License/Terms of Use:


## Use Case:

Developers, coordinators, and protocol operators use this skill to translate natural language requests into crunch-cli commands for CrunchDAO coordinator, competition, staking, reward, checkpoint, and cruncher account workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet-backed commands can move, drain, stake, withdraw, delegate, create, start, or end protocol state and funds.

Mitigation: Require the agent to show the exact command, active profile, wallet public address, network/RPC, target, token, amount, and expected effect, then obtain explicit confirmation before execution.

Risk: Using the wrong Solana network, RPC endpoint, wallet path, or profile can direct actions to the wrong account or environment.

Mitigation: Prefer devnet and dry runs where available, and verify the active profile, wallet public address, network, and RPC endpoint before any state-changing command.

Risk: Global npm installation introduces package supply-chain and version drift risk.

Mitigation: Install only @crunchdao/crunch-cli from the official npm registry after user consent, and pin or verify the package version before installing.

## Reference(s):

- [Coordinator CLI Full Reference](references/cli-reference.md)
- [Crunch CLI npm package](https://www.npmjs.com/package/@crunchdao/crunch-cli)
- [ClawHub skill page](https://clawhub.ai/philippwassibauer/skills/crunch-coordinate)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and formatted text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May format responses for Slack, Telegram, Discord, or plain text.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
