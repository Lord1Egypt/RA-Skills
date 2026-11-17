## Description:

Alpha Finder (x402) researches prediction markets across Polymarket, Kalshi, and other sources to produce market intelligence, probability assessments, sentiment analysis, and arbitrage leads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tzannetosgiannis](https://clawhub.ai/user/tzannetosgiannis)

### License/Terms of Use:


## Use Case:

External users and market researchers use this skill to query prediction-market data and commentary, assess probabilities and sentiment, and identify possible mispriced or arbitrage opportunities before trading or research decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a wallet private key and passes it to a third-party npm package downloaded at runtime.

Mitigation: Use a dedicated low-balance Base wallet, avoid primary wallet keys, restrict plaintext config file permissions, and prefer a pinned, reviewed package version or safer signing flow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tzannetosgiannis/skills/alpha-finder)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text or Markdown market research response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [$0.03 USDC per request via x402 on Base; requires a wallet private key through X402_PRIVATE_KEY or x402-config.json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
