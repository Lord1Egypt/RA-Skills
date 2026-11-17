## Description:

Provides professional cryptocurrency investment and strategy analysis for spot, swing, and leverage decisions, combining technical analysis, market regime assessment, position sizing, staged entry and exit planning, portfolio allocation, and risk control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codeblackhole1024](https://clawhub.ai/user/codeblackhole1024)

### License/Terms of Use:

Apache 2.0

## Use Case:

External users and developers use this skill for cryptocurrency decision support: buy, sell, hold, reduce, rotate, allocate, rank assets, and draft risk-aware trading or portfolio plans. Outputs should be treated as informational and probabilistic, not guaranteed predictions or a substitute for independent financial review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live market data used for trading recommendations can be tampered with because HTTPS certificate checks are disabled in the market-data script.

Mitigation: Treat outputs as informational only, verify market data with trusted sources before acting, and review the data-fetching script before use.

Risk: The README includes a --break-system-packages dependency installation path.

Mitigation: Install dependencies in an isolated virtual environment instead of modifying the system Python environment.

Risk: Snapshot logging can store trade-analysis history locally.

Mitigation: Enable snapshot logging or output files only when local storage of trading analysis is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/codeblackhole1024/skills/crypto-investment-strategist)
- [Allocation Playbook](references/allocation-playbook.md)
- [Asset Scoring](references/asset-scoring.md)
- [Market Regimes](references/market-regimes.md)
- [Portfolio Construction](references/portfolio-construction.md)
- [Position Planning](references/position-planning.md)
- [Review Workflow](references/review-workflow.md)
- [Risk Framework](references/risk-framework.md)
- [Tokenomics Checklist](references/tokenomics-checklist.md)
- [Workflow Orchestration](references/workflow-orchestration.md)
- [Numpy Migration Plan](references/numpy-migration-plan.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands and optional JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fetch live market data, calculate indicators, rank assets, allocate capital, and optionally write local JSON outputs or analysis snapshot logs.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
