## Description:

A lightweight ECharts-based charting skill that helps agents turn structured data into static chart images with reusable style configuration and direct PNG export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ykforerlang](https://clawhub.ai/user/ykforerlang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to generate line, bar, pie, gauge, area, dual-axis, scatter, radar, and funnel charts from CSV, JSON, tables, metrics, or SQL-like results. It is best suited for static report graphics, dashboard-style visuals, and chart assets that need configurable styling without a browser runtime.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs npm runtime dependencies before rendering charts.

Mitigation: Install from trusted sources, prefer pinned versions, and run npm install and rendering without unnecessary secrets or elevated privileges.

Risk: The linked configuration page is external to the local skill package.

Mitigation: Avoid entering confidential labels, business data, or sensitive chart content into the external page.

Risk: Returned update-config payloads can overwrite persistent chart defaults.

Mitigation: Review config payloads before persistence and only apply updates that match the intended chart type and style contract.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ykforerlang/skills/data-charts-visualization)
- [Configuration page](https://ykforerlang.github.io/awesome-skills/skills-helpler/data-charts-visualization/web/index.html)
- [CLI and config contract](references/cli-and-config.md)
- [Chart selection and variants](references/chart-selection-and-variants.md)
- [Config page handoff](references/config-page-handoff.md)
- [Chart config presets](config/README.md)

## Skill Output:

**Output Type(s):** [files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands, JSON configuration, and generated PNG or SVG file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rendered charts default to PNG and use skill-local config presets unless the user requests another supported output or style.]

## Skill Version(s):

1.0.13 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
