## Description:

DexScan Skill helps an agent retrieve on-chain market data, including token prices and details, token signals, social heat, and smart-money address data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yishixing01](https://clawhub.ai/user/yishixing01)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent query DexScan for token rankings, token details, market activity, K-line history, address PnL, portfolio holdings, and smart-money leaderboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DexScan credentials may be loaded from .env files in parent directories, which can use keys not intended for this skill.

Mitigation: Run the skill in an isolated directory tree without unrelated .env files, or require credential loading to use only explicit environment variables or a fixed skill-local .env file.

Risk: Token, wallet, and tweet queries are sent to DexScan with the configured DexScan API credentials.

Mitigation: Use credentials approved for DexScan requests and avoid submitting sensitive token, wallet, or tweet queries unless that sharing is acceptable.

## Reference(s):

- [DexScan OpenAPI](https://openapi.dexscan.trade)
- [Token API Reference](references/coin.md)
- [Address API Reference](references/address.md)
- [Market API Reference](references/market.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or structured text summarizing DexScan API results, with JSON-like fields from DexScan responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Formats time and numeric fields; paginated endpoints may include cursor continuation prompts.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
