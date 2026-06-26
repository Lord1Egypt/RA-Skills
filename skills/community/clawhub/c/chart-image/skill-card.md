## Description: <br>
Generate publication-quality line, bar, area, point, histogram, candlestick, pie/donut, heatmap, multi-series, and stacked chart images from data for reports, alerts, and time-series visualizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dannyshmueli](https://clawhub.ai/user/dannyshmueli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn structured data into local chart image files for dashboards, reports, alerts, and shared messages. It is designed for headless server deployments where browser-based chart rendering is undesirable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the skill runs npm dependency installation for the bundled chart renderer. <br>
Mitigation: Review the included dependency manifest and lockfile before production installation, and install only in environments where those dependencies are acceptable. <br>
Risk: User-controlled chart data, titles, labels, or file paths could be mishandled if they are interpolated into shell commands. <br>
Mitigation: Invoke the chart script with structured argv-style process execution, pass data as JSON or through trusted temporary files, and keep output/spec paths controlled by the runtime. <br>
Risk: Generated charts may contain sensitive data if the source dataset is sensitive. <br>
Mitigation: Send chart images only to intended channels or storage locations, and avoid sharing sensitive chart outputs unless that disclosure is intended. <br>


## Reference(s): <br>
- [Chart Image on ClawHub](https://clawhub.ai/dannyshmueli/chart-image) <br>
- [README](artifact/README.md) <br>
- [Capability Definition](artifact/CAPABILITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Images, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [PNG or SVG chart image files generated from JSON data, with Markdown and shell-command guidance for setup and invocation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates charts locally with Node.js, Vega-Lite, and Sharp; chart/spec/output paths should remain runtime-controlled.] <br>

## Skill Version(s): <br>
2.6.35 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
