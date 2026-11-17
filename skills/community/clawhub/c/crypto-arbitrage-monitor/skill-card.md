## Description:

Monitors ETH crypto arbitrage signals by checking funding rates and basis opportunities across exchanges, then produces a Chinese-language buy, wait, or risk signal report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pcy891](https://clawhub.ai/user/pcy891)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to gather live ETH funding-rate and arbitrage context and summarize potential spot-perpetual or cross-exchange opportunities. It is intended as a monitoring and signal-reporting aid, not as a substitute for independent financial analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce actionable crypto trading recommendations from broad arbitrage or funding-rate prompts.

Mitigation: Use the output only as a monitoring aid and require independent review before any trading decision.

Risk: The evidence security summary identifies a material annualized-return error in the template example.

Mitigation: Recalculate annualized returns from live funding rates and verify fees, slippage, and timestamps before relying on reported yields.

Risk: Funding rates and spreads can change quickly and may reverse before settlement.

Mitigation: Verify current exchange data immediately before opening or closing positions and monitor for negative funding-rate changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pcy891/skills/crypto-arbitrage-monitor)
- [Publisher profile](https://clawhub.ai/user/pcy891)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with exchange funding-rate table, overall rating, strategy guidance, timing note, and risk warnings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language output; relies on current market data searches and requires independent verification of rates, fees, slippage, timestamps, and annualized-return math.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version note)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
