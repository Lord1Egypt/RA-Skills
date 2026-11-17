## Description:

Trade Polymarket weather markets using NOAA and Open-Meteo forecasts through the Simmer API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richducat](https://clawhub.ai/user/richducat)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading agents use this skill to configure, dry-run, monitor, or execute automated Polymarket temperature-market trades based on weather forecasts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can automate real-money Polymarket trades with wallet signing authority.

Mitigation: Keep dry-run as the default, use a dedicated low-balance wallet, and verify automaton limits before enabling live trading.

Risk: Credential exposure could compromise Simmer API access or wallet funds.

Mitigation: Store SIMMER_API_KEY and WALLET_PRIVATE_KEY only in environment or secret storage, and do not paste private keys into chat or logs.

Risk: Live-trading safeguards are weak and can be disabled.

Mitigation: Keep safeguards enabled, avoid --no-safeguards, and review slippage, liquidity, position-size, and scheduling settings before live operation.

Risk: The skill depends on simmer-sdk for trading behavior.

Mitigation: Pin and review simmer-sdk before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/richducat/skills/dolph-weather-trader)
- [Simmer Dashboard](https://simmer.markets/dashboard)
- [Simmer API](https://api.simmer.markets)
- [NOAA Weather API](https://api.weather.gov)
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default execution is dry-run; live trading requires explicit flags and credentials.]

## Skill Version(s):

1.0.0 (source: target metadata and server release metadata; artifact metadata reports 1.17.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
