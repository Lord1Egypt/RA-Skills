## Description:

Extracts structured knowledge from PDF books and helps generate editable HTML or Markdown infographics for concepts, chapter summaries, timelines, comparisons, flows, and charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luemery](https://clawhub.ai/user/luemery)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to turn PDF books into structured summaries and editable visual aids for study, research, teaching, or content analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML may run remote JavaScript and include PDF-derived text in active HTML or JavaScript contexts.

Mitigation: Open generated HTML locally, escape or sanitize PDF-derived text, and serialize chart data safely before sharing.

Risk: Processing sensitive or untrusted PDFs may expose document contents or unsafe generated output.

Mitigation: Review the skill before use with sensitive documents and avoid processing untrusted PDFs unless output escaping is verified.

Risk: The HTML template loads ECharts from a public CDN.

Mitigation: Vendor ECharts locally or add integrity and content-security controls before distributing generated infographics.

## Reference(s):

- [Book Infographic ClawHub Page](https://clawhub.ai/luemery/skills/book-infographic)
- [Infographic Guide](references/infographic-guide.md)
- [ECharts Documentation](https://echarts.apache.org/zh/index.html)
- [Chart.js Documentation](https://www.chartjs.org/docs/)
- [D3.js Documentation](https://d3js.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JSON snippets, shell commands, and editable HTML or Markdown infographic output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce intermediate PDF extraction JSON and editable infographic files; generated HTML should be reviewed before sharing.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
