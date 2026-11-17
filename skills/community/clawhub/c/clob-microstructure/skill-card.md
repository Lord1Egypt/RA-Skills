## Description:

Analyzes Polymarket CLOB order books to score liquidity gaps, order book imbalance, whale activity, and fake breakouts, generating trading signals and optionally executing mean-reversion trades when run in live mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mibayy](https://clawhub.ai/user/mibayy)

### License/Terms of Use:

MIT-0

## Use Case:

Traders and agent operators use this skill to scan active Polymarket markets for order-book microstructure inefficiencies, review signals, and optionally run controlled mean-reversion trades through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real trades when run with --live and a valid Simmer API key.

Mitigation: Keep dry-run mode until the strategy is trusted, use a dedicated API key with limited permissions and spending limits, and review live settings before unattended use.

Risk: Unpinned dependencies may change behavior over time.

Mitigation: Pin simmer-sdk and requests versions before unattended live use.

## Reference(s):

- [Polymarket CLOB Book API endpoint](https://clob.polymarket.com/book)
- [Polymarket Trades Data API endpoint](https://data-api.polymarket.com/trades)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Console logs and summary text with command-line usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to dry-run mode; live trading requires --live and SIMMER_API_KEY.]

## Skill Version(s):

2.0.6 (source: server evidence, SKILL.md frontmatter, clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
