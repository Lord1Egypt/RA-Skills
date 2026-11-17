## Description:

A-share portfolio optimization skill that helps agents collect asset constraints, estimate returns and risk, run quantitative portfolio optimization methods, and present allocation weights, risk contribution, and efficient-frontier results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzswk](https://clawhub.ai/user/yzswk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate A-share portfolio allocation analysis from a user-provided asset pool, constraints, and historical return data. It supports mean-variance, minimum-variance, risk-parity, equal-weight, and documented Black-Litterman workflows for formal reports or brief optimization summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portfolio allocations are generated from historical data and user-supplied assumptions, so results may be misleading if treated as investment advice or future performance forecasts.

Mitigation: Review financial assumptions, input data quality, risk-free-rate settings, and constraints before relying on the output; present outputs as decision support rather than investment advice.

Risk: The documented Black-Litterman workflow is broader than the current command-line interface exposed by the optimizer script.

Mitigation: Confirm whether Black-Litterman inputs are handled manually or by additional tooling before promising automated CLI execution for that method.

## Reference(s):

- [A股组合优化参考手册](references/portfolio-optimize-guide.md)
- [ClawHub skill page](https://clawhub.ai/yzswk/skills/a-share-portfolio-optimize)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown reports with tables, shell command snippets, and JSON optimizer output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce formal multi-section analysis or a brief optimization summary; script output includes asset statistics, correlations, optimization results, and optional efficient-frontier points.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
