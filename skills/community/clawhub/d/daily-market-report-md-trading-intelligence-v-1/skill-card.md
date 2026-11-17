## Description:

Creates concise daily market intelligence reports that combine macro, market-structure, timing, and risk inputs into ranked manual trading opportunities and wait guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sarkcesscrewpay](https://clawhub.ai/user/sarkcesscrewpay)

### License/Terms of Use:

MIT-0

## Use Case:

Traders and market analysts use this skill to turn upstream market brief, pattern recognition, timeframe, and risk assessment outputs into a daily Markdown report for manual trade planning. It supports scheduled session updates, high-confidence alerts, and wait warnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market reports can be misleading if the upstream market data or event context is incomplete, stale, or incorrect.

Mitigation: Verify market data, macro events, spreads, volatility, and structure independently before using the report for trade planning.

Risk: Trading outputs could be misused as automatic trade instructions.

Mitigation: Keep manual control of any trades and do not connect the skill directly to trading or messaging automation without separate safeguards.

Risk: Missing or conflicting inputs can create false confidence in a setup.

Mitigation: Use the skill's WAIT posture when required confirmations are absent, risk is elevated, or the structure is unclear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sarkcesscrewpay/skills/daily-market-report-md-trading-intelligence-v-1)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown daily market intelligence reports, session updates, alerts, and wait warnings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Decision-support output for manual execution; expects verified market, structure, timing, and risk inputs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
