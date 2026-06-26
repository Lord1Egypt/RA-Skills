## Description: <br>
Analyzes tabular data, recommends suitable chart types, and generates an interactive HTML dashboard with Plotly visualizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cloudcba](https://clawhub.ai/user/cloudcba) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to turn CSV or Excel data into an interactive dashboard when they need chart recommendations and quick visual exploration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML may preserve source data and visualizations in a local file. <br>
Mitigation: Review the generated file before sharing and avoid sensitive personal or business data unless local persistence is acceptable. <br>
Risk: The chart-generation script writes to the output path supplied by the user. <br>
Mitigation: Choose a safe output path and confirm it will not overwrite an important file. <br>


## Reference(s): <br>
- [Chart Types Guide](references/chart-types.md) <br>
- [Data Format Guide](references/data-format.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/cloudcba/data-visualization-cloud) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Shell commands, Guidance] <br>
**Output Format:** [HTML dashboard file with terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads CSV or Excel input and saves a single responsive Plotly HTML dashboard; generated charts are capped at 15.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
