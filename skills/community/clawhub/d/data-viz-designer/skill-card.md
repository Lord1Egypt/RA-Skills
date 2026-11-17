## Description:

A data visualization designer that transforms complex data into clear, intuitive charts and visualizations, covering data exploration and analysis, chart type selection, layout and style design, detail tuning, and interactive feature addition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to turn raw datasets into clear charts, infographics, and browser-ready visualizations. It helps select appropriate chart types, tune visual design, and add useful interactions such as filters, zooming, and hover tooltips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser-ready chart files may embed sensitive or private datasets directly in generated output.

Mitigation: Review generated files before sharing and remove or anonymize sensitive data that should not be distributed.

Risk: Generated HTML may load third-party chart libraries from a CDN.

Mitigation: Review external script URLs and replace them with approved local or pinned dependencies when required by deployment policy.

Risk: Visualization choices can make trends, proportions, or comparisons misleading if chart type, scaling, or labels are poorly matched to the data.

Mitigation: Validate chart type, axes, labels, annotations, and color choices against the source data before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openlark/skills/data-viz-designer)
- [Publisher profile](https://clawhub.ai/user/openlark)
- [ECharts CDN example dependency](https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown or complete HTML/CSS/JavaScript code, with SVG or PNG output when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include embedded datasets, chart configuration, rendering logic, and optional browser-based interactivity.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
