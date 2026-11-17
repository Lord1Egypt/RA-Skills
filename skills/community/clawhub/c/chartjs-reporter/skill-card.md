## Description:

Turns structured data such as query results, CSV summaries, JSON records, or Python dicts/lists into standalone dark-themed HTML visualization reports powered by Chart.js.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cloudcba](https://clawhub.ai/user/cloudcba)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data analysts, and agents use this skill to convert structured tabular or JSON-like data into browser-viewable Chart.js reports with KPI cards and common chart types. It is useful after SQL, DuckDB, pandas, CSV, or manual data analysis when the user wants a shareable HTML visualization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML can execute untrusted report data as JavaScript.

Mitigation: Use trusted data only, escape HTML-sensitive text fields, and validate chart and table inputs before generation or preview.

Risk: Generated reports load Chart.js from a CDN.

Mitigation: Bundle or pin Chart.js locally, or add integrity protection and clearly disclose the network dependency.

Risk: Automatically previewing untrusted reports can expose users to unsafe HTML behavior.

Mitigation: Review generated HTML first and open untrusted reports only in a controlled browser context.

## Reference(s):

- [Chart.js chart configuration guide](references/chart-config-guide.md)
- [Theme tokens](references/theme-tokens.md)
- [Report generation script](scripts/generate_report.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON chart configuration, Python or shell command examples, and generated standalone HTML report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports use a dark theme, Chart.js 4.4.0 from CDN, responsive chart grids, KPI cards, and optional tables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
