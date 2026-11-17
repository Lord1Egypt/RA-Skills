## Description:

Byreal Perps CLI helps agents guide users through Hyperliquid perpetual futures account setup, market and limit orders, position management, leverage controls, trade history, and market signal analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ggg223399](https://clawhub.ai/user/ggg223399)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to have an agent operate the Byreal CLI for Hyperliquid perpetual futures workflows, including account checks, order and position commands, leverage changes, and public market signal scans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents toward high-impact live trading actions such as opening orders, changing leverage, and closing positions.

Mitigation: Use testnet first and require explicit user confirmation of account, side, coin, size, price, leverage, and order intent before any write action.

Risk: Broad delegation such as asking an agent to manage trades can create unclear authority over financial decisions.

Mitigation: Limit delegation to specific, user-confirmed commands and have the agent restate the proposed action before execution.

Risk: The global Node package install and update flow can change the executable used by the agent.

Mitigation: Pin or verify the CLI package version before installation or update, especially before using commands that affect live positions.

Risk: Private keys or agent wallet credentials could be mishandled if requested in chat.

Mitigation: Direct users to run the CLI account initialization flow interactively and never ask them to paste private keys into the conversation.

## Reference(s):

- [Byreal Perps CLI GitHub Repository](https://github.com/byreal-git/byreal-perps-cli)
- [Byreal Perps CLI on ClawHub](https://clawhub.ai/ggg223399/skills/byreal-perps-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose account setup, read-only market or account queries, trading commands, testnet usage, and troubleshooting steps.]

## Skill Version(s):

0.2.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
