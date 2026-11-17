## Description:

Calculate asset allocation weights for a portfolio of ETFs based on Risk Parity (All Weather) principles, including annualized return and risk metrics with interactive agent guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wzwangyc](https://clawhub.ai/user/wzwangyc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to generate ETF allocation guidance based on risk parity, historical lookback settings, investment amount, and a configurable ETF pool. It supports portfolio tables, annualized return and volatility estimates, and optional report outputs for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependencies are not fully pinned in the artifact.

Mitigation: Install the skill in an isolated Python environment and use reviewed pinned dependencies or a lockfile before operational use.

Risk: The skill contacts external market-data services, so results can depend on data availability, service behavior, and current market data.

Mitigation: Review generated allocations and metrics against trusted market data before making decisions.

Risk: The default configuration uses Chinese/CNY assumptions and local ETF defaults.

Mitigation: Confirm currency, ETF pool, and lookback period with the user before running the analysis.

Risk: The CLI report-saving path can create local CSV and PDF files.

Mitigation: Use report export only when local file creation is intended and verify the output directory before sharing files.

Risk: Portfolio outputs may be mistaken for guaranteed investment advice.

Mitigation: Present allocations, return estimates, and volatility metrics as informational analysis that requires human financial review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wzwangyc/skills/all-weather-strategy)
- [ClawHub publisher profile](https://clawhub.ai/user/wzwangyc)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance, files]

**Output Format:** [Markdown or text guidance with Python usage snippets, allocation tables, metrics, charts, and optional CSV/PDF report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses external market-data services and Chinese/CNY defaults; generated financial outputs are informational and require user review.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
