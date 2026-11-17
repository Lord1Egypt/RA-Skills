## Description:

Analyzes crypto token supply dilution risk by comparing circulating supply against max/total supply using the free CoinGecko API, computes dilution scores and risk labels, and outputs either a readable table or JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and crypto researchers use this skill to run quick tokenomics due diligence on future supply dilution by CoinGecko ID or by scanning top market-cap coins. It is a supply-side risk proxy and not an investment recommendation or project-specific vesting unlock calendar.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Coin IDs and top-N scan choices are sent to CoinGecko when the tool fetches market data.

Mitigation: Use the skill only when sharing those query choices with CoinGecko is acceptable, and consider adding an explicit CoinGecko network allowlist in stricter environments.

Risk: Dilution scores are based on circulating, total, and max supply fields and do not include project-specific vesting cliffs or unlock schedules.

Mitigation: Treat the output as a supply-side screening signal and confirm material decisions with project disclosures, token unlock calendars, and independent financial analysis.

Risk: CoinGecko free-tier availability and rate limits can affect live data retrieval.

Mitigation: Retry later, reduce scan size, or cache results when running repeated due-diligence checks.

## Reference(s):

- [CoinGecko Markets API endpoint](https://api.coingecko.com/api/v3/coins/markets)
- [ClawHub skill page](https://clawhub.ai/ssidharhubble/skills/crypto-supply-dilution-tracker)

## Skill Output:

**Output Type(s):** [text, JSON, analysis, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples; runtime output is a terminal table or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses CoinGecko public market data; no API key or package installation is required.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
