## Description:

Trading Quant helps agents fetch and analyze real-time market data for A-shares, U.S. and Hong Kong stocks, precious metals, market anomalies, capital flows, and quantitative scoring signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to retrieve live market data and produce quantitative trading analysis, market scans, capital-flow summaries, and risk-marked signal labels for finance research and monitoring workflows. Outputs should be treated as informational analysis, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill calls multiple public market and news APIs and exposes a broad command-line analysis surface.

Mitigation: Install only where those external requests are acceptable, review commands before execution, and limit use to trusted agent workflows.

Risk: Local temp and cache handling needs review before installation, especially on shared multi-user systems.

Mitigation: Run as a non-privileged user and avoid shared multi-user hosts until temp, cache, and batch-output handling are hardened.

Risk: Trading scores and signal labels can be mistaken for investment recommendations.

Mitigation: Treat outputs as informational analysis and require qualified human review before financial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onlyloveher/skills/cn-stock-analyzer)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and structured market-analysis results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market data and scoring results depend on external public data sources and local cache freshness.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
