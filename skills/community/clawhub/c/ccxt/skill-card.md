## Description:

Interact with 100+ cryptocurrency exchanges to fetch markets, order books, tickers, place orders, check balances, and more using the CCXT CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pcriadoperez](https://clawhub.ai/user/pcriadoperez)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to query cryptocurrency exchange market data, inspect account state, and prepare or execute CCXT CLI trading workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned trading CLI and can use exchange API keys for immediate financial actions.

Mitigation: Review before installing, test with sandbox mode, prefer read-only API keys, enable trading permissions only when needed, and disable withdrawals and transfers.

Risk: Order creation and cancellation methods can execute immediately when valid credentials are configured.

Mitigation: Confirm exchange, symbol, side, amount, price, and order or cancellation intent immediately before running trading commands.

## Reference(s):

- [CCXT Documentation](https://docs.ccxt.com)
- [ClawHub Skill Page](https://clawhub.ai/pcriadoperez/skills/ccxt)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend raw JSON output from the ccxt CLI for programmatic parsing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
