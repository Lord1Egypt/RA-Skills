## Description: <br>
Renders JSON data, Markdown tables, or ECharts options into PNG, SVG, JPEG, or WebP chart images using a bundled ECharts and Sharp script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kadbbz](https://clawhub.ai/user/kadbbz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert structured data or complete ECharts options into chart image files for reports, user responses, or downstream file transfer. It is intended for chart generation from JSON, Markdown tables, or existing ECharts configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency resolution and native image-processing packages can affect reproducibility across installs. <br>
Mitigation: Install from a release that includes the lockfile and use the pinned dependency set when possible. <br>
Risk: Generated chart files and optional ECharts option files are written to caller-provided output paths. <br>
Mitigation: Write outputs inside the workspace chart_output directory and review paths before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kadbbz/skills/aios-make-chart-image) <br>
- [Publisher profile](https://clawhub.ai/user/kadbbz) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, Guidance] <br>
**Output Format:** [Image files with stdout JSON status and optional saved ECharts option JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports PNG, SVG, JPEG, and WebP output; default canvas size is 1200x800.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
