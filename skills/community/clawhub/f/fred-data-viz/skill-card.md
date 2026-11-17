## Description:

Create publication-ready economic comparison charts from Federal Reserve Economic Data (FRED) for visualizing, comparing, and analyzing macroeconomic time series.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pratyushchauhan](https://clawhub.ai/user/pratyushchauhan)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts, researchers, and developers use this skill to configure and generate indexed comparison charts for FRED economic time series, including wage, GDP, inflation, employment, and profit indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The chart script contacts FRED with the configured series IDs and date ranges.

Mitigation: Use only public, non-sensitive series choices and date ranges in chart configurations.

Risk: The chart script can overwrite the output file path selected by the user.

Mitigation: Choose a deliberate output path and check for existing files before running chart generation.

## Reference(s):

- [Federal Reserve Economic Data (FRED)](https://fred.stlouisfed.org)
- [FRED Data Viz on ClawHub](https://clawhub.ai/pratyushchauhan/skills/fred-data-viz)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands, Files]

**Output Format:** [Markdown guidance with JSON configuration examples, bash commands, and a generated chart image file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches public FRED CSV data and writes the requested chart output path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
