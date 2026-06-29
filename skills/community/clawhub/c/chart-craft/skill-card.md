## Description: <br>
数据描述转柱状图/折线图/饼图等8种交互式SVG图表HTML <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwbwin](https://clawhub.ai/user/wwbwin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and business users use this skill to turn natural-language or tabular data descriptions into lightweight interactive chart HTML for documents, email, and reports. It supports bar, line, pie, donut, area, stacked bar, radar, and combo chart patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Included HTML templates are placeholders, so generated output may depend on the agent following the chart specification rather than a complete implementation. <br>
Mitigation: Review generated chart HTML before reuse and verify that the rendered chart accurately represents the provided data. <br>
Risk: Generated chart HTML may contain inline CSS, JavaScript, SVG, or Canvas code derived from user-provided data. <br>
Mitigation: Use local, trusted data inputs and inspect generated HTML before embedding it in documents, email, or reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wwbwin/skills/chart-craft) <br>
- [Publisher project homepage](https://github.com/wwbwin/clawhub-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with single-file HTML, inline CSS, JavaScript, and SVG chart code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated charts are intended to be zero-dependency local HTML using inline assets and system fonts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
