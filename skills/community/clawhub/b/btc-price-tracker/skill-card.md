## Description:

Tracks live Bitcoin prices, shows USD, CNY, and SGD values, manages local price alerts, and emits Telegram-style notification text from a command-line workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[siemen90](https://clawhub.ai/user/siemen90)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to check current Bitcoin prices, maintain local above-or-below price alerts, and review alert notifications in a CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing with the optional sudo symlink can place the script on a shared system path.

Mitigation: Install and run the skill from a virtual environment, and avoid the sudo symlink unless an administrator has reviewed the target path.

Risk: Bundled sample alert data and user-created alert names may reveal trading intent if notifications are forwarded through Telegram.

Mitigation: Review or delete bundled sample alerts, and avoid sensitive trading details in alert names when Telegram delivery is enabled.

Risk: The dependency declaration allows a broad requests version range.

Mitigation: Pin dependencies before production use and refresh them through the normal dependency review process.

Risk: CoinGecko rate limits or request failures can produce delayed checks or fallback cached prices.

Mitigation: Use modest polling intervals, monitor request failures, and verify market data before making financial decisions.

## Reference(s):

- [CoinGecko API](https://www.coingecko.com/en/api)
- [ClawHub skill page](https://clawhub.ai/siemen90/skills/btc-price-tracker)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Command-line text output and local JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores alerts and cached price data in local JSON files; notification delivery depends on the surrounding OpenClaw or Telegram setup.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
