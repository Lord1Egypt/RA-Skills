## Description: <br>
Automatically analyzes CSV or JSON data, recommends chart combinations, and generates interactive HTML dashboards with chart views, theme switching, table previews, and statistical summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to turn tabular CSV or JSON data into an HTML dashboard with recommended charts, summary statistics, and a raw-data preview. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated dashboards can turn crafted CSV or JSON content into active browser code when opened. <br>
Mitigation: Use trusted datasets or a restricted workspace, avoid opening dashboards generated from unknown files, and escape or render user data as text in safer versions. <br>
Risk: Dashboard HTML can contain raw source data. <br>
Mitigation: Treat generated HTML as sensitive, review it before sharing, and avoid uploading confidential datasets unless the output handling is acceptable. <br>
Risk: The generated HTML loads Chart.js from a CDN. <br>
Mitigation: Use a local or integrity-pinned Chart.js asset where network trust, reproducibility, or supply-chain controls are required. <br>


## Reference(s): <br>
- [Chart Selection Rules](references/chart-selection.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/openlark/ai-data-visualizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated HTML dashboard files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated dashboards may include raw input data and load Chart.js from a CDN.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
