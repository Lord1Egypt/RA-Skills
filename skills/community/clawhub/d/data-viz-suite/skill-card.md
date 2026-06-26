## Description: <br>
Data Viz Suite helps agents generate charts, interactive dashboards, and business reports using Plotly, Matplotlib, Seaborn, and common tabular data sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent builders use this skill to create data visualizations, dashboards, and exportable reports from CSV, Excel, JSON, SQL, or pandas-style data inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency versions are broad and may change behavior or introduce supply-chain exposure over time. <br>
Mitigation: Install in an isolated Python environment and pin dependency versions before production use. <br>
Risk: Generated HTML dashboards or reports can expose unsafe content if untrusted data is inserted without escaping. <br>
Mitigation: Sanitize or escape untrusted data before exporting HTML. <br>
Risk: Generated dashboards may fetch Plotly JavaScript from a CDN when opened. <br>
Mitigation: Review network access requirements and use approved offline or pinned assets where required. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/openclaw/skills/tree/main/data-viz-suite) <br>
- [ClawHub skill page](https://clawhub.ai/kaiyuelv/data-viz-suite) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with Python snippets and generated chart, dashboard, or report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files may include HTML, PDF, PNG, and Excel outputs; dashboards may rely on Plotly JavaScript from a CDN.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
