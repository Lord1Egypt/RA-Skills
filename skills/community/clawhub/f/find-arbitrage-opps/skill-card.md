## Description:

Find arbitrage opportunities across exchanges by comparing prices for fungible token pairs like BTC/WBTC and USDT/USDC.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengtality](https://clawhub.ai/user/fengtality)

### License/Terms of Use:


## Use Case:

Developers and trading operators use this skill to scan Hummingbot-connected exchanges for candidate arbitrage opportunities across fungible token pairs. It helps compare connector prices, identify best buy and sell venues, and filter opportunities by spread or connector.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The prerequisite setup command executes a remote script through curl-to-bash.

Mitigation: Review or replace the prerequisite command before running it.

Risk: Default API credentials and environment-loaded settings could point the scanner at an unintended Hummingbot API.

Mitigation: Set explicit non-default API credentials, keep HUMMINGBOT_API_URL on localhost or HTTPS, and check which .env file is being loaded.

Risk: The scanner retrieves market data from configured exchange connectors and may produce misleading opportunities if connectors or API responses are stale or untrusted.

Mitigation: Run it only against a trusted local Hummingbot API with configured exchange connectors and review results before acting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fengtality/skills/find-arbitrage-opps)
- [Hummingbot Prerequisite Script](https://raw.githubusercontent.com/hummingbot/skills/main/skills/lp-agent/scripts/check_prerequisites.sh)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Terminal text summary or JSON with prices, outliers, and arbitrage opportunities]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires base and quote token inputs; optional connector filter, minimum spread threshold, and JSON output mode.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
