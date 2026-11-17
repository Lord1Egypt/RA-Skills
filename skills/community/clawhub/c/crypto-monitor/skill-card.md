## Description:

Cryptocurrency market monitoring with real-time prices, on-chain data, whale tracking, and alerting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawto](https://clawhub.ai/user/clawto)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to retrieve cryptocurrency market prices, review whale-transfer activity, identify trending tokens, and check airdrop information through shell-based API queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that one script can automatically modify the host system by attempting package installation.

Mitigation: Review before installing and run in a low-privilege environment; install dependencies explicitly rather than allowing automatic package changes.

Risk: The security scan reports that multiple shell options can be abused to run unintended commands before numeric arguments are validated.

Mitigation: Validate and constrain option values before passing them to scripts, especially numeric flags such as limits, thresholds, and watch intervals.

Risk: The skill depends on live cryptocurrency and airdrop data from external APIs that can be unavailable, rate-limited, stale, or misleading.

Mitigation: Treat outputs as informational, verify market and airdrop claims independently, and avoid using responses as the sole basis for financial or wallet actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawto/skills/crypto-monitor)
- [ClawHub publisher profile](https://clawhub.ai/user/clawto)
- [CoinGecko API endpoint](https://api.coingecko.com/api/v3)
- [DeFiLlama airdrops endpoint](https://api.llama.fi/airdrops)
- [Whale Alert transactions endpoint](https://api.whale-alert.io/v1/transactions)
- [Etherscan API endpoint](https://api.etherscan.io/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and text, JSON, or CSV script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live third-party cryptocurrency APIs and may be subject to provider availability, data freshness, and rate limits.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
