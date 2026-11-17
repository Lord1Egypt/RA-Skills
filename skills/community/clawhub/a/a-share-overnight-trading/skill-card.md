## Description:

Provides A-share main-board overnight trading guidance for screening one stock near the market close, holding it overnight, and selling at the next open with defined risk controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jokerzeng](https://clawhub.ai/user/jokerzeng)

### License/Terms of Use:

MIT-0

## Use Case:

External traders and agents use this skill to structure an educational A-share overnight trading workflow, including stock screening, position sizing, mock backtesting, and risk discipline. It is not a reliable stock-picking system or financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mock backtest outputs may look like actionable trading results even though they are based on synthetic data.

Mitigation: Use verified market data and independent review before any real trading decision; treat mock results as educational examples only.

Risk: Backtest scripts write predictable files under /tmp.

Mitigation: Run scripts in an isolated environment and inspect or remove generated /tmp files after use, especially on shared systems.

Risk: Overnight equity trading can cause financial loss, including gap-down, liquidity, and halt risks.

Mitigation: Use paper trading first, limit position size, and consult qualified financial advice before committing capital.

## Reference(s):

- [Screening Criteria](references/screening_criteria.md)
- [Risk Management](references/risk_management.md)
- [Case Studies](references/case_studies.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with optional Python CLI commands and script-generated reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate mock backtest text, CSV, and chart files when scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
