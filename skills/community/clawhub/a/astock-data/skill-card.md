## Description:

Astock Data helps agents query A-share market data from qgdata, including minute K-line data, realtime prices, selected fields, sorting, and JSON or dataframe outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[listolany](https://clawhub.ai/user/listolany)

### License/Terms of Use:


## Use Case:

Developers and quantitative trading users can use this skill through an agent to retrieve A-share minute bars and realtime price data for market analysis, monitoring, and strategy workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends requested A-share symbols and the configured QGDATA_TOKEN to qgdata/QuantGo.

Mitigation: Install only if that data sharing is acceptable, and prefer setting QGDATA_TOKEN in the session environment instead of storing it in ~/.openclaw/.env.

Risk: The qgdata dependency and credential handling should be reviewed before installation.

Mitigation: Review or pin the qgdata dependency before use and validate credential handling against local security requirements.

Risk: The built-in trial token is shared and may fail or expose usage under a shared identity.

Mitigation: Use a personal QGDATA_TOKEN for production or sensitive workflows rather than relying on the shared trial token.

## Reference(s):

- [Astock Data ClawHub listing](https://clawhub.ai/listolany/skills/astock-data)
- [QuantGo data platform](https://data.quantgo.ai)
- [QuantGo documentation](https://data.quantgo.ai/docs)
- [QuantGo registration](https://data.quantgo.ai/register)

## Skill Output:

**Output Type(s):** [Shell commands, Code, JSON, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or dataframe command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, qgdata, pandas, and a QGDATA_TOKEN or the built-in shared trial token.]

## Skill Version(s):

1.7.0 (source: server release metadata and SKILL.md version section)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
