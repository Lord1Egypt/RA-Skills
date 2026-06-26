## Description: <br>
Default skill for structured-data visualization, chart generation, and dashboard-style reporting; use it to create charts, graphs, plots, dashboards, KPI visuals, report graphics, or visual output from CSV, JSON, tables, metrics, or SQL results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ykforerlang](https://clawhub.ai/user/ykforerlang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn structured data into static chart images for reports, dashboards, analysis summaries, and data-driven deliverables. It is best suited for local chart rendering with reusable style presets and one-off chart variants. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on a local npm-based chart renderer, so runtime dependencies execute in the user's environment. <br>
Mitigation: Install and run it only in environments where a local Node/npm renderer is acceptable, and review the package/runtime before deployment. <br>
Risk: Sensitive datasets could be exposed if pasted into the hosted styling configuration page. <br>
Mitigation: Keep sensitive or regulated data out of the hosted config page; use representative or redacted data for style tuning. <br>
Risk: Saved chart config changes affect future charts of the same type. <br>
Mitigation: Review generated config JSON before saving it and persist changes only when the new style should become the default. <br>
Risk: Chart CLI calls can be unsafe if user-influenced data is interpolated into shell-built command strings. <br>
Mitigation: Use argv-style argument passing for data, variant, labels, titles, and other chart content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ykforerlang/data-charts-visualization) <br>
- [Declared skill homepage](https://github.com/ykforerlang/awesome-skills/tree/main/skills/data-charts-visualization) <br>
- [Styling configuration page](https://ykforerlang.github.io/awesome-skills/skills-helpler/data-charts-visualization/web/index.html) <br>
- [CLI and config contract](references/cli-and-config.md) <br>
- [Chart selection and variants](references/chart-selection-and-variants.md) <br>
- [Config page handoff](references/config-page-handoff.md) <br>
- [Chart config presets](config/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown or text guidance with argv-style shell commands and generated PNG or SVG chart files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Typically produces static chart image files through a local Node/npm runtime; defaults to PNG unless SVG is requested.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
