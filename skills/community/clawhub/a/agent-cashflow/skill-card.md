## Description:

Track real revenue for ClawHub skill publishers, including installs, downloads, stars, and optional ETH wallet balance from live APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[infectit007](https://clawhub.ai/user/infectit007)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and ClawHub skill publishers use this skill to assemble portfolio performance reports from ClawHub stats and optional Ethereum wallet data. It can also provide cashflow report content for daily agent briefings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ETH tracking sends wallet addresses to public RPC providers.

Mitigation: Use ETH tracking only when the publisher is comfortable sharing the wallet address with those providers.

Risk: Scheduled reports may forward financial details to Telegram and memory.

Mitigation: Avoid the Telegram and memory cron prompt unless that storage and forwarding behavior is intended.

Risk: The artifact encourages starring skills from multiple accounts.

Mitigation: Do not follow reputation manipulation guidance; use legitimate publication and promotion practices.

Risk: The skill may overstate wallet privacy.

Mitigation: Review the examples before use and treat wallet addresses and report contents as potentially exposed to external services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/infectit007/skills/agent-cashflow)
- [Ethereum LlamaRPC endpoint](https://eth.llamarpc.com)
- [Ankr Ethereum RPC endpoint](https://rpc.ankr.com/eth)
- [CoinGecko ETH price endpoint](https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON, Bash, and Python examples; generated reports are plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated ClawHub CLI for ClawHub stats; ETH tracking is optional and uses public RPC and price APIs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
