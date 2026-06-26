## Description: <br>
ECharts Master designs and generates professional interactive ECharts HTML visualizations from user-provided table, JSON, CSV, or query-result data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Linux2010](https://clawhub.ai/user/Linux2010) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to turn tabular, JSON, CSV, or query-result data into ECharts chart HTML, choose suitable chart types, and preview the result locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated chart files may include sensitive source data. <br>
Mitigation: Generate charts in a dedicated folder and review files before sharing or serving them. <br>
Risk: The local preview server can expose chart files beyond the intended viewer if bound too broadly or left running. <br>
Mitigation: Serve only the chart folder, bind the server to 127.0.0.1 when possible, and stop the preview server when finished. <br>


## Reference(s): <br>
- [ECharts chart design guide](references/chart-design.md) <br>
- [ECharts HTML base template](assets/echarts-base-template.html) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Code, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with HTML, JavaScript, ECharts option objects, JSON examples, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local HTML chart files and localhost preview instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
