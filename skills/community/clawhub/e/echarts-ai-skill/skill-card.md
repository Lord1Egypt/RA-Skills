## Description: <br>
Generate charts from natural language or tabular data, recommend chart types, and export ECharts-based HTML or SVG. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davaded](https://clawhub.ai/user/davaded) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn user-supplied chart requests or tabular data into deterministic ECharts options and exportable chart artifacts for reports, previews, and dashboards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML previews and demos may contact third-party CDNs. <br>
Mitigation: Use SVG output or locally bundled assets when operating offline or under stricter supply-chain controls. <br>
Risk: Chart recommendations or field mappings can be incorrect for ambiguous or underspecified data. <br>
Mitigation: Review generated chart specs and provide explicit fields or chart types when accuracy matters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/davaded/echarts-ai-skill) <br>
- [Project Homepage](https://github.com/davaded/Echarts-AI-Skill) <br>
- [Project Repository](https://github.com/davaded/Echarts-AI-Skill) <br>
- [ECharts Documentation](https://echarts.apache.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON chart specifications, ECharts option JSON, HTML previews, SVG files, and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated HTML previews may load ECharts from a third-party CDN; SVG output is available for more self-contained artifacts.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release metadata; artifact metadata reports 0.1.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
