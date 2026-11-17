## Description:

Real-time crypto prices and technical indicators such as RSI, MACD, Bollinger Bands, EMA, and SMA using public Binance and CoinGecko market-data APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for cryptocurrency market prices, ticker statistics, candlestick data, common technical indicators, and multi-symbol scans from public market-data sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that one command can run arbitrary local code when given a crafted pair filter.

Mitigation: Review before installing, and avoid running the pairs command with untrusted or generated filter text until the interpolation issue is fixed.

Risk: Market data and indicator outputs are time-sensitive and may be incomplete or unavailable when public API calls fail.

Mitigation: Treat outputs as technical reference data, verify important trading or financial decisions against authoritative sources, and handle failed API responses before relying on results.

Risk: The release evidence notes that the advertised indicator count and no-ads claim are overstated.

Mitigation: Present the skill as supporting the concrete indicators evidenced in the artifact, including RSI, MACD, Bollinger Bands, EMA, and SMA.

## Reference(s):

- [BytesAgain Homepage](https://bytesagain.com)
- [ClawHub Skill Listing](https://clawhub.ai/xueyetianya/skills/bytesagain-crypto)
- [Binance Public API](https://api.binance.com/api/v3)
- [CoinGecko API](https://api.coingecko.com/api/v3)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text with shell command examples and tabular market-data output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call public external market-data APIs and return time-sensitive cryptocurrency prices or indicator values.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
