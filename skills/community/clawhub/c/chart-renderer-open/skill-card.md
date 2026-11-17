## Description:

Render structured data into polished, self-contained HTML pages with heatmaps, trend lines, category cards, styled tables, and more. Screenshot/download ready. Suitable for reports, dashboards, comparisons, and analyses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dachunggan](https://clawhub.ai/user/dachunggan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn structured data into self-contained HTML chart reports, including heatmaps, line charts, category cards, styled tables, and text callouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports are active HTML pages, and report data may execute injected browser code.

Mitigation: Review or sanitize untrusted data before rendering, and avoid opening or sharing generated reports with sensitive same-origin access until HTML-safe data embedding and escaping are verified.

Risk: Generated reports may rely on external browser dependencies for chart rendering and downloads.

Mitigation: Pin, vendor, or otherwise control Chart.js, ChartDataLabels, and html2canvas dependencies for managed deployments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dachunggan/skills/chart-renderer-open)
- [Project Homepage](https://github.com/dachunggan/chart-renderer-open)

## Skill Output:

**Output Type(s):** [files, code, markdown, configuration]

**Output Format:** [Self-contained HTML report files with JSON configuration/data blocks and a Markdown embed snippet]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated pages may include browser-executed JavaScript and CDN-loaded visualization dependencies.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
