## Description: <br>
Chart.js charting skill. Used to generate visual charts such as line charts, bar charts, pie charts, radar charts, scatter plots, etc. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate Chart.js visualizations from user-provided data, including chart setup, configuration, and output options for HTML, screenshots, or image files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated chart code may load Chart.js through npm or a CDN that is not allowed in every project environment. <br>
Mitigation: Confirm the target project's dependency policy before installing npm packages or using CDN-loaded Chart.js. <br>
Risk: Generated HTML or JavaScript may be run with private or sensitive visualization data. <br>
Mitigation: Review generated HTML and JavaScript before execution and avoid exposing sensitive data in shared browser, screenshot, or export workflows. <br>


## Reference(s): <br>
- [Chart.js API Reference](references/api.md) <br>
- [Chart.js CDN package](https://cdn.jsdelivr.net/npm/chart.js) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline HTML, JavaScript, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose complete HTML for browser rendering or code suitable for screenshot/PDF/image export.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
