## Description:

Provides CLI-backed crypto market leaderboards for social hype, trending and top-search tokens, Binance Alpha and tokenized-stock ranks, smart-money inflows, Pulse meme scores, and top trader PnL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binance-skills-hub](https://clawhub.ai/user/binance-skills-hub)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve ranked Binance Web3 crypto token and wallet leaderboards for market discovery, social sentiment, smart-money inflow, meme-token scoring, and trader PnL questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may pass private wallet notes, credentials, or unrelated personal data as command parameters.

Mitigation: Use the skill only for public crypto token and address ranking questions, and avoid sending secrets or unrelated personal data.

Risk: Live crypto rankings can be volatile and should not be treated as investment advice.

Mitigation: Treat outputs as informational market data and verify important decisions with authoritative financial and risk-review processes.

Risk: Network failures, rate limits, or unsupported chain and parameter combinations can interrupt leaderboard retrieval.

Mitigation: Check CLI exit codes and error messages, use documented chain and period values, and retry transient failures with appropriate backoff.

## Reference(s):

- [CLI Reference](references/cli.md)
- [ClawHub Skill Page](https://clawhub.ai/binance-skills-hub/skills/binance-web3-crypto-market-rank)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or text summaries supported by JSON CLI output from public Binance Web3 API calls.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI returns live public market ranking data; numeric market fields may need parsing before calculations.]

## Skill Version(s):

3.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
