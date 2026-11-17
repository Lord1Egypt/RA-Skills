## Description:

Generate charts from natural language or tabular data, recommend chart types, and export ECharts-based HTML or SVG.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davaded](https://clawhub.ai/user/davaded)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn natural-language or table-shaped chart requests into deterministic ECharts options and exportable HTML or SVG previews. It supports chart recommendation, explicit chart generation, and writing chart artifacts to requested output paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML previews may embed chart data into executable browser script when rendering untrusted or shared inputs.

Mitigation: Review generated HTML before opening or hosting it, prefer SVG for untrusted data, and require safe escaping before publishing HTML previews.

Risk: HTML previews load ECharts from a CDN.

Mitigation: Use a pinned or locally bundled ECharts dependency in environments that require supply-chain control or offline operation.

Risk: Export commands write files to disk and can overwrite selected output paths.

Mitigation: Use explicit output directories, review target paths before execution, and avoid running exports in directories with important existing artifacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/davaded/skills/echarts-ai-skill)
- [Project repository](https://github.com/davaded/Echarts-AI-Skill)
- [ECharts documentation](https://echarts.apache.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands; generated JSON, HTML, or SVG chart artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files use default names such as spec.json, option.json, preview.html, and preview.svg unless an explicit output path is provided.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
