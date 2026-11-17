## Description:

Predict funding trend shifts using NLP analysis of grant abstracts from NIH, NSF, and Horizon Europe.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research strategy analysts use this skill to run NLP-based grant abstract analysis, generate reports, and review forecast-style funding trend summaries across NIH, NSF, and Horizon Europe.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Synthetic or forecast-style funding analysis may be mistaken for verified funding intelligence.

Mitigation: Treat outputs as exploratory and verify conclusions against authoritative agency data before using them for decisions.

Risk: Unpinned Python dependencies create avoidable install-time supply-chain risk.

Mitigation: Install in an isolated environment, pin and review dependencies, and run dependency auditing before deployment.

Risk: The script writes generated reports to a user-provided output path.

Mitigation: Run in a sandboxed workspace and review output paths before execution.

## Reference(s):

- [Funding Trend Forecaster on ClawHub](https://clawhub.ai/aipoch-ai/skills/funding-trend-forecaster)
- [NIH RePORTER](https://reporter.nih.gov/)
- [NSF Award Search](https://www.nsf.gov/awardsearch/)
- [EU Funding & Tenders Portal](https://ec.europa.eu/info/funding-tenders/opportunities/)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell and Python examples; runtime output is JSON or plain text reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script accepts CLI parameters for source selection, analysis period, forecast horizon, output path, and output format.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
