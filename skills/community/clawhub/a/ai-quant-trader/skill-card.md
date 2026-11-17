## Description:

Ai Quant Trader helps an agent simulate A-share stock screening, technical analysis, strategy generation, backtesting, automated trading, and risk-management workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuhuijiang2025-cell](https://clawhub.ai/user/yuhuijiang2025-cell)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to explore simulated quantitative trading workflows, including stock screening, strategy drafting, paper-trade execution, stop-loss and take-profit rules, and portfolio risk review. Outputs should be treated as simulation and decision support, not as validated financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screening, backtest, strategy-performance, and signal outputs can be mistaken for validated financial analysis.

Mitigation: Treat these outputs as simulation only unless the publisher replaces random placeholders with validated data sources and documented methodology.

Risk: Dependency installation and registration scripts can modify the local environment or overwrite prior skill files.

Mitigation: Run installation in an isolated environment and review backup and path behavior before rerunning registration.

Risk: Automated trading flows could be misused with a real broker integration.

Mitigation: Do not connect to a real broker without explicit confirmations, path validation, audit logs, and hard trading limits.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuhuijiang2025-cell/skills/ai-quant-trader)
- [Artifact Skill Documentation](artifact/SKILL.md)
- [Quick Start Guide](artifact/QUICK_START.md)
- [Simplified Conversation Mode](artifact/SIMPLIFIED_SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and text responses with command examples, plus Python and JSON files when the local scripts are used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces simulated finance analysis and may cache or save local user, strategy, position, and screening data.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
