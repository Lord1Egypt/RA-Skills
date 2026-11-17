## Description:

APEX IA Pro provides Binance Futures market scanning and trading workflow guidance using SMA 8/21, Pivot SuperTrend, RSI, volume, and multi-timeframe confluence signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcusfranca12](https://clawhub.ai/user/marcusfranca12)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-tool users use this skill to scan Binance Futures markets for ranked setup signals, configure scanner parameters, and review generated trading guidance before taking any action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence classifies this release as suspicious because it contains under-disclosed automated Binance Futures trading programs with leveraged execution paths.

Mitigation: Do not install or run trader scripts unless automated trading is intentional, live/testnet mode is confirmed, and explicit controls exist for order confirmation, leverage, stop loss, and account permissions.

Risk: The security evidence reports embedded Binance credentials in packaged trading programs.

Mitigation: Rotate any exposed credentials before use and restrict any replacement credentials to the minimum permissions and environment needed for the intended scanner or trading workflow.

Risk: The skill produces financial-market signals and trading guidance that can be incorrect or unsuitable for the user's account and risk tolerance.

Mitigation: Treat outputs as analysis only, independently verify signals, and start with testnet or paper trading before considering live Binance Futures activity.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marcusfranca12/skills/apex-ia-pro)
- [Publisher profile](https://clawhub.ai/user/marcusfranca12)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with trading signals, setup commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include ranked Binance Futures symbols, indicator scores, target and stop values, and environment variable examples.]

## Skill Version(s):

3.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
