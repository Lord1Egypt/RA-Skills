## Description: <br>
Generate Apple HIG-inspired HTML visualizations for bar, line, donut, progress, horizontal bar, and stat-card charts, then capture them as PNG images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baderfahoum17](https://clawhub.ai/user/baderfahoum17) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn structured chart data into Apple-style PNG visualizations for reports, dashboards, and summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill renders user-provided chart data through local browser screenshot tooling. <br>
Mitigation: Use trusted or sanitized chart data and run the skill in an environment appropriate for local browser execution. <br>
Risk: The output path is caller-controlled and the skill writes PNG files to that location. <br>
Mitigation: Choose output paths deliberately and avoid overwriting important files. <br>
Risk: The release depends on browser tooling and an unpinned pyppeteer dependency. <br>
Mitigation: Pin dependencies before use in sensitive or reproducible environments. <br>


## Reference(s): <br>
- [Apple Viz ClawHub skill page](https://clawhub.ai/baderfahoum17/skills/apple-viz) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands] <br>
**Output Format:** [PNG image file path, with command-line invocation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports light and dark mode, custom width and height, and JSON data schemas for supported chart types.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
