## Description:

Tools and techniques for detrending time series data in macroeconomic analysis. Use when working with economic time series that need to be decomposed into trend and cyclical components. Covers HP filter, log transformations for growth series, and correlation analysis of business cycles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and researchers use this skill to prepare macroeconomic time series for business-cycle analysis by separating trend and cyclical components, applying appropriate log transforms, and computing cyclical correlations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned Python dependencies can produce different analysis behavior across environments.

Mitigation: Install statsmodels, pandas, and numpy in a virtual environment and pin versions for reproducible or organization-controlled analysis.

Risk: Incorrect detrending choices can lead to misleading macroeconomic cycle interpretation.

Mitigation: Verify the data frequency before selecting the HP-filter lambda, and avoid log transforms for series with zeros, negative values, or rate-style measurements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/econ-detrending-correlation-timeseries-detrending)
- [Publisher profile](https://clawhub.ai/user/wu-uk)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides package installation guidance and example Python snippets for HP filtering, log transformation, and correlation analysis.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
