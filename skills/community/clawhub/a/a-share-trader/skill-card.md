## Description:

A Share Trader is an adaptive quantitative trading framework for China A-share market analysis that combines stock-selection strategies, market-state recognition, dynamic strategy weighting, and risk controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmaya](https://clawhub.ai/user/hmaya)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading-system reviewers use this skill to inspect, simulate, or adapt an A-share quantitative trading framework with multiple stock-selection strategies and adaptive risk controls. Its outputs should be treated as development or simulation support, not as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading and live-mode framing could be mistaken for deployable trading automation.

Mitigation: Use the skill only for inspection, simulation, or paper trading unless live mode is disabled by default and every real order requires explicit user confirmation.

Risk: Synthetic or fallback market data can make analysis and signals unreliable.

Mitigation: Require verified real-data provenance before relying on any generated signal, backtest, or portfolio metric.

Risk: Weak or incomplete risk gates may allow unsafe trading assumptions.

Mitigation: Review risk controls, make them fail closed, and require human approval before connecting any brokerage or execution pathway.

## Reference(s):

- [README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/hmaya/skills/a-share-trader)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python snippets, shell commands, and JSON-style status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include trading signals, simulated portfolio metrics, strategy settings, and risk-control guidance; outputs require human review before any real trading use.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
