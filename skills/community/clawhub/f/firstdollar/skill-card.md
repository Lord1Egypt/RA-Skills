## Description:

First Dollar is a curriculum that teaches AI agents how to understand wallets, USDC, x402 payment challenges, and payment troubleshooting while explaining commands instead of signing transactions for the agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lisamaraventano-spine](https://clawhub.ai/user/lisamaraventano-spine)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to learn how to inspect wallets, interpret x402 payment challenges, choose compatible payment networks, and troubleshoot failed agent-initiated purchases. It is educational guidance for agents using their own wallets and funds, not a delegated payment or signing service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet and payment commands could trigger real transfers or route funds to an unintended merchant, chain, recipient, asset, or amount.

Mitigation: Before running any suggested command, manually verify the merchant, network, recipient, asset, amount, and maximum spend; use a test wallet with a very small balance for learning and first payments.

Risk: Private keys or wallet secrets could be exposed through pasted prompts, printed environment values, or command-line arguments.

Mitigation: Do not paste or print private keys, redact wallet secrets from prompts and logs, and avoid passing private keys directly on command lines.

Risk: Unpinned npx or package-install commands may execute versions other than the reviewed release.

Mitigation: Pin package versions before using npx or npm install, and review the exact package and version before execution.

## Reference(s):

- [First Dollar on ClawHub](https://clawhub.ai/lisamaraventano-spine/skills/firstdollar)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown text with inline shell commands, JSON snippets, and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single textual response per tool call; some responses include commands the agent may choose to run.]

## Skill Version(s):

1.0.4 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
