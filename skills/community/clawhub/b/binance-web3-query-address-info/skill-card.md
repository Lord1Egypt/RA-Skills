## Description:

Snapshot of a single wallet's token holdings on a specific chain, including token name, symbol, current price, 24-hour price change, and holding quantity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binance-skills-hub](https://clawhub.ai/user/binance-skills-hub)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to inspect the current public token holdings for a supplied EVM or Solana wallet address on supported chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses and chain IDs entered into the skill are sent to Binance Web3 to retrieve public portfolio data.

Mitigation: Use the skill only when the queried address can be associated with that external request.

Risk: Results depend on a live external Binance Web3 endpoint and may fail for unsupported chains, malformed addresses, network failures, or rate limiting.

Mitigation: Validate address and chain inputs, include the required offset parameter, and handle documented CLI exit codes and Binance business codes.

## Reference(s):

- [CLI Reference](references/cli.md)
- [ClawHub Skill Page](https://clawhub.ai/binance-skills-hub/skills/binance-web3-query-address-info)
- [Publisher Profile](https://clawhub.ai/user/binance-skills-hub)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON response fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI returns JSON from the Binance Web3 endpoint and uses paginated offsets for wallet holdings.]

## Skill Version(s):

2.0.0 (source: server release evidence; artifact frontmatter version is 2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
