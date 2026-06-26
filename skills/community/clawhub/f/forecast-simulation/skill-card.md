## Description: <br>
Provides a Chinese-language workflow for simple trend extrapolation, target gap analysis, what-if simulation, and depletion or saturation forecasting from existing metric data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackyujun](https://clawhub.ai/user/jackyujun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and business operators use this skill to reason about future metric values, target feasibility, what-if scenarios, and resource depletion based on historical business data returned by a trusted metric-query skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Forecasting can expose or rely on sensitive business metrics. <br>
Mitigation: Use the skill only with trusted metric-query workflows and treat metric inputs and outputs as sensitive business data. <br>
Risk: Simple mathematical forecasts can be mistaken for machine-learning predictions or precise commitments. <br>
Mitigation: Present assumptions, uncertainty, rounded values, and ranges; call out trend breaks, seasonality, promotions, holidays, and long forecast horizons. <br>
Risk: Broad routing language may trigger forecasting for ambiguous planning requests. <br>
Mitigation: Ask a clarifying question when intent is unclear between ordinary discussion, historical metric lookup, and future-facing forecasting or simulation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jackyujun/forecast-simulation) <br>
- [Publisher profile](https://clawhub.ai/user/jackyujun) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown guidance with example JSON query parameters and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Forecast outputs should include assumptions, uncertainty notes, and rounded estimates or ranges rather than false precision.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
