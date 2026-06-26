## Description: <br>
Trade Polymarket weather markets using NOAA (US) and Open-Meteo (international) forecasts via Simmer API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richducat](https://clawhub.ai/user/richducat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading-oriented agents use this skill to configure, monitor, and optionally execute Polymarket weather-market trades based on weather forecasts and user-defined risk limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trade with real funds when live mode and wallet credentials are enabled. <br>
Mitigation: Keep dry-run mode enabled until the strategy is reviewed, use a dedicated low-balance wallet, and set conservative max position and max trades values. <br>
Risk: Wallet private keys and API keys may be exposed if stored in shared or plaintext environments. <br>
Mitigation: Store credentials only in an appropriate secret store or private environment and avoid logging or sharing them. <br>
Risk: Unattended live runs can place trades without direct user review. <br>
Mitigation: Avoid enabling scheduling or quiet live runs until the user has reviewed the strategy and is comfortable with unattended trading risk. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/richducat/dolph-weather-trader) <br>
- [Simmer API](https://api.simmer.markets) <br>
- [Simmer dashboard](https://simmer.markets/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Console text, optional JSON status reports, and Markdown setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can execute live trades only when explicitly run in live mode with required credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact metadata describes 1.17.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
