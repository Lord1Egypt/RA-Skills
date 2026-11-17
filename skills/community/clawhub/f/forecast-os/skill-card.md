## Description:

Forecast the future on Polymarket, Kalshi, and Precog. Check live markets before answering what is likely to happen. Use when the user asks about odds, event outcomes, or prediction markets; wants to discover, quote, buy, sell, fund, or claim; create and fund a market to obtain real info when none is available; fund a launchpad/upcoming market; claim investment/incentive funding rewards; install and configure forecast; or needs first-time setup, a relayer, a Precog private key, a Kalshi API key, an RSA PEM, or a missing forecast binary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xastraea](https://clawhub.ai/user/0xastraea)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this agent skill to check live prediction market odds and discover markets, then get guidance for quoting, trading, creating, funding, or claiming through ForecastOS. It also guides setup of the Forecast CLI and its credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: This trading skill can install software silently and let its publisher force updates without approval while handling wallet credentials.

Mitigation: Require visible approval for installation and each update, pin reviewed versions, and keep wallet secrets in restricted local files rather than chat. Use a dedicated wallet and check the amount, token, chain, and recipient before approving transactions; externally downloaded CLI behavior remains unverified.

## Reference(s):

- [ForecastOS on ClawHub](https://clawhub.ai/0xastraea/skills/forecast-os)
- [Forecast CLI releases](https://github.com/precog-markets/forecast-os/releases)
- [ForecastOS on skills.sh](https://skills.sh/precog-markets/forecast-os)
- [Command reference](artifact/skills/forecast-os/references/commands.md)
- [Configuration and authentication](artifact/skills/forecast-os/references/config-and-auth.md)
- [Pitfalls reference](artifact/skills/forecast-os/references/pitfalls.md)
- [Quote and buy workflow](artifact/skills/forecast-os/workflows/quote-and-buy.md)
- [Manage positions workflow](artifact/skills/forecast-os/workflows/manage-positions.md)
- [Create Precog market workflow](artifact/skills/forecast-os/workflows/create-precog-market.md)
- [Fund launchpad workflow](artifact/skills/forecast-os/workflows/fund-launchpad.md)
- [Update workflow](artifact/skills/forecast-os/workflows/update.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Text summaries and JSON market results, with Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market results and transaction previews may be included; actions that submit trades, funding, claims, or market creation require user approval.]

## Skill Version(s):

2.0.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
