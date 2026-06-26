## Description: <br>
Trade Kalshi prediction markets through conversation, powered by Fuku sports model predictions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cryptopunk2070](https://clawhub.ai/user/cryptopunk2070) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to browse Kalshi sports prediction markets, compare prices against Fuku model predictions, build trading profiles, and prepare or execute trades within configured risk limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can interact with a real Kalshi account and place live trades, including unattended operation. <br>
Mitigation: Start in dry-run or approval mode, keep auto-trading disabled unless explicitly intended, and use the configured daily loss, position size, and trade count limits. <br>
Risk: Kalshi credentials are stored locally in a .env file. <br>
Mitigation: Protect the .env file, exclude it from commits and sync tools, and rotate credentials if exposure is suspected. <br>
Risk: Balances, profiles, orders, positions, and trade history may be shown in chat output or written to local files. <br>
Mitigation: Run the skill only in trusted local workspaces and review generated logs or chat transcripts before sharing them. <br>
Risk: Model probabilities and edge estimates can be wrong or become stale as markets and sports information change. <br>
Mitigation: Review each recommendation, current market price, and risk setting before trade execution. <br>


## Reference(s): <br>
- [Fuku Predictions ClawHub page](https://clawhub.ai/cryptopunk2070/fuku-predictions) <br>
- [Kalshi API credentials](https://kalshi.com/profile/api) <br>
- [Fuku Public Prediction API](https://cbb-predictions-api-nzpk.onrender.com) <br>
- [Kalshi Sports Markets Guide](references/kalshi-markets.md) <br>
- [Trading Strategies Reference](references/strategies.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal output with JSON configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include market prices, model probabilities, edge estimates, payout estimates, trading recommendations, profile settings, account balances, positions, and local trade logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
