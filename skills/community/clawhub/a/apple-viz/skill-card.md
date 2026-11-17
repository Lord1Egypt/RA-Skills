## Description:

Generate Apple HIG-inspired HTML visualizations for bar, line, donut, progress, and stat-card charts, then save them as PNG screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baderfahoum17](https://clawhub.ai/user/baderfahoum17)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use Apple Viz to turn provided JSON data into polished PNG chart files for reports, dashboards, and quick visual summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-controlled chart data is rendered in a browser and may include unescaped fields.

Mitigation: Use isolated execution with non-sensitive or trusted chart data; escape user-controlled fields and validate colors and numeric inputs before broader deployment.

Risk: Screenshot rendering can fall back to an unsandboxed Chromium path and uses unpinned runtime dependencies.

Mitigation: Keep browser sandboxing enabled where possible, restrict browser and network behavior, and pin dependencies before production use.

## Reference(s):

- [Apple Viz ClawHub skill page](https://clawhub.ai/baderfahoum17/skills/apple-viz)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [PNG image file plus a printed output path; on screenshot failure, a temporary HTML path may be printed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports light and dark mode, custom image dimensions, and bar, line, donut, progress, horizontal bar, and stat-card chart types.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
