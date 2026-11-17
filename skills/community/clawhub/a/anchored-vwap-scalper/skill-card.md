## Description:

Runs an Anchored VWAP BTC scalping workflow for Lighter DEX using Python strategy scripts, ccxt market data, and optional live order placement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidm413](https://clawhub.ai/user/davidm413)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and traders can use this skill to configure, dry-run, and operate BTC-USD scalping logic against Lighter DEX. The skill is intended for users who can review automated trading behavior and manage exchange API credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place live crypto exchange orders and server security evidence says its safety claims and controls are not reliable enough for live funds without review.

Mitigation: Use dry-run mode first, independently test exchange order semantics, restrict API keys to minimum trading permissions, remove withdrawal authority where possible, and risk only collateral you are willing to lose.

Risk: The artifact advertises fixed risk, daily loss, leverage, stop-loss, and take-profit controls, but server guidance says those claims should not be relied on without code fixes and live-exchange validation.

Mitigation: Review the strategy code and validate stop-loss, take-profit, leverage, position sizing, and daily loss behavior in a controlled environment before enabling live trading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/davidm413/skills/anchored-vwap-scalper)
- [Publisher profile](https://clawhub.ai/user/davidm413)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and Python execution details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call exchange APIs and may write local state and log files when executed.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 1.6.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
