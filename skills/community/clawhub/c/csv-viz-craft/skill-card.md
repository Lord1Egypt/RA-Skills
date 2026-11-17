## Description:

CSV数据转可筛选、排序、搜索的交互式数据表格HTML

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwbwin](https://clawhub.ai/user/wwbwin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to turn pasted CSV or TSV data into shareable interactive single-file HTML tables, dashboards, comparisons, chart views, and print-ready reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pasted CSV data may include secrets, personal identifiers, financial records, or confidential business fields.

Mitigation: Review and minimize CSV input before use, removing sensitive fields that are not required for the visualization.

Risk: Generated defaults and template language may be Chinese-language unless adapted.

Mitigation: Localize labels, prompts, and output text for the intended audience before sharing generated HTML.

Risk: The artifact's HTML template files are placeholders, so generated output behavior may depend on agent-authored implementation.

Mitigation: Review the generated HTML for correct parsing, filtering, sorting, export, and display behavior before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwbwin/skills/csv-viz-craft)
- [Project homepage](https://github.com/wwbwin/clawhub-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance and self-contained HTML code with inline CSS and JavaScript]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended as single-file HTML visualizations; bundled artifact templates are placeholders in this version.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
