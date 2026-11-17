## Description:

Trade Kalshi prediction markets through conversation, powered by Fuku sports model predictions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptopunk2070](https://clawhub.ai/user/cryptopunk2070)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to define prediction-market trading preferences, scan Kalshi sports markets with Fuku model edges, review recommendations, and optionally place or exit trades within configured risk limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real-money Kalshi trades automatically.

Mitigation: Use dry-run or approval mode by default and enable full-auto trading only after reviewing the configuration, limits, and expected financial exposure.

Risk: Kalshi credentials may be stored in a local plaintext `.env` file.

Mitigation: Protect or replace plaintext credential storage, restrict file access, and use API keys with the minimum permissions and spending limits required.

Risk: Recurring scheduled trading can continue to execute without active user review.

Mitigation: Avoid full-auto cron trading unless the operator understands the financial risk, monitors activity, and maintains a tested stop or kill-switch process.

## Reference(s):

- [Fuku Predictions ClawHub Release](https://clawhub.ai/cryptopunk2070/skills/fuku-predictions)
- [Kalshi Sports Markets Guide](references/kalshi-markets.md)
- [Trading Strategies Reference](references/strategies.md)
- [Configuration README](config/README.md)
- [Fuku Prediction API](https://cbb-predictions-api-nzpk.onrender.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text recommendations, JSON configuration and profile files, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include market prices, model probabilities, edge estimates, payout math, profile summaries, and local trading actions when configured.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
