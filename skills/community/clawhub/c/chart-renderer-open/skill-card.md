## Description: <br>
Renders structured data into polished, self-contained HTML reports with heatmaps, trend lines, category cards, styled tables, screenshot export, and download-ready output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dachunggan](https://clawhub.ai/user/dachunggan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn provided structured data into self-contained HTML chart and report pages for analysis, dashboards, comparisons, and sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports are active HTML and may execute malicious content if untrusted or unsanitized data is inserted into the report. <br>
Mitigation: Use the skill only with trusted or sanitized input data, especially when content comes from copied web pages, uploads, emails, or third-party text. <br>
Risk: Rendered canvas previews or hosted report files may expose sensitive report contents if shared or stored in an unexpected location. <br>
Mitigation: Confirm where previews and generated HTML files are stored before sharing reports that include confidential data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dachunggan/chart-renderer-open) <br>
- [Project homepage](https://github.com/dachunggan/chart-renderer-open) <br>
- [Chart type registry](templates/registry.json) <br>
- [Page template](templates/chart_page.html) <br>
- [Heatmap format](templates/types/heatmap.md) <br>
- [Line chart format](templates/types/line.md) <br>
- [Dual-axis chart format](templates/types/dualAxis.md) <br>
- [Layered cards format](templates/types/layered.md) <br>
- [Recommendation cards format](templates/types/direction.md) <br>
- [Table format](templates/types/table.md) <br>
- [Text block format](templates/types/text.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, HTML, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance plus self-contained HTML report files assembled from JSON data, CSS, and JavaScript templates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include hosted report preview embed markup and downloadable screenshot behavior.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
