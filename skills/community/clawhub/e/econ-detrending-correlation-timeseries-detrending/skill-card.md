## Description: <br>
Tools and techniques for detrending time series data in macroeconomic analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and economics researchers use this skill to decompose macroeconomic time series into trend and cyclical components, select HP-filter smoothing parameters by data frequency, and compare business-cycle correlations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the recommended Python packages can introduce dependency or environment risk. <br>
Mitigation: Use a virtual environment and verify package sources before installing statsmodels, pandas, and numpy. <br>
Risk: HP-filter outputs can be misleading when the data frequency, lambda value, or log transform is inappropriate for the series. <br>
Mitigation: Confirm the series frequency, use the matching smoothing parameter, and avoid log transforms for series with zeros, negative values, or rate units. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/econ-detrending-correlation-timeseries-detrending) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides analytical guidance and example commands; it does not execute code or access external services by itself.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
