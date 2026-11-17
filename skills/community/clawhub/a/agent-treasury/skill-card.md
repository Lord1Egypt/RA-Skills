## Description:

Manage your agent's crypto wallet. Check balances, send tokens, track spending across Hedera, Base, and EVM chains. Built for agents who earn and spend on-chain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imaflytok](https://clawhub.ai/user/imaflytok)

### License/Terms of Use:


## Use Case:

Agents and developers use this skill to inspect crypto balances, track bounty income and spending, check gas prices, and prepare wallet operation commands across Hedera, Base, and EVM chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mainnet transfer examples can move real assets if account credentials, recipient, network, or amount are wrong.

Mitigation: Require explicit human review before transfer execution, prefer testnet first, and use low-value accounts for initial runs.

Risk: Private keys or operator credentials could be pasted into source files or command history.

Mitigation: Keep secrets out of source files, avoid committing credentials, and use a dedicated secret store or reviewed local environment variables.

Risk: The skill contains unexplained external OADP registration and ping endpoints.

Mitigation: Do not allow a host to auto-consume those endpoints unless the publisher and destination are trusted and the user has approved the network behavior.

Risk: The HBAR transfer example recommends a global unpinned SDK install.

Mitigation: Install dependencies locally where possible and pin or review SDK versions before using wallet operations.

## Reference(s):

- [Agent Treasury on ClawHub](https://clawhub.ai/imaflytok/skills/agent-treasury)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Markdown, Configuration, Guidance]

**Output Format:** [Markdown with bash and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes wallet balance checks, local ledger examples, gas checks, and HBAR transfer guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
