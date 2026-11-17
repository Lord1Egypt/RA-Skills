## Description:

Analyzes China A-share K-line data with real-time quotes, historical K-line data, technical indicators, candlestick patterns, volume analysis, structured reports, scoring, and next-day trend forecasts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amatuer718](https://clawhub.ai/user/amatuer718)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to run command-line technical analysis for China A-share stock symbols, producing reports, JSON data, and optional chart files for review. Outputs should be treated as educational technical analysis, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install command uses --break-system-packages, which can modify system Python packages.

Mitigation: Install the skill in an isolated virtual environment and avoid system-level package installation.

Risk: Unpinned Python dependencies and external finance data sources may change behavior over time.

Mitigation: Review and pin dependencies before deployment, and validate outputs against trusted market data.

Risk: Generated trading suggestions and next-day forecasts may be mistaken for investment advice.

Mitigation: Treat outputs as educational technical analysis only and require human review before any financial decision.

Risk: Some advertised features may not work exactly as documented.

Mitigation: Run representative commands during acceptance testing and document any unsupported or changed behavior.

## Reference(s):

- [A-Stock Kline Analyzer ClawHub page](https://clawhub.ai/amatuer718/skills/a-stock-kline-analyzer)
- [Sina Finance](https://finance.sina.com.cn)
- [Sina Finance realtime quote endpoint](https://hq.sinajs.cn/list={sina_code})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Command-line text reports, JSON records, Python code, shell commands, and optional chart image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses stock code, period, day count, realtime/report/JSON flags, and optional chart output path.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
