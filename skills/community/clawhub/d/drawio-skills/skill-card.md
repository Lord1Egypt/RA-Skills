## Description:

DrawIO 图表技能 helps agents generate .drawio architecture, flow, ER, UML, sequence, network topology, and ML diagrams, extract reusable style presets from existing DrawIO files, apply the linlan style, and optionally export diagrams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linlannet](https://clawhub.ai/user/linlannet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and technical writers use this skill to create DrawIO diagrams for architecture, process, data model, topology, and ML workflows. They can also analyze existing .drawio files to extract drawing style presets and reuse a documented linlan visual style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled style_report.json may expose internal infrastructure details.

Mitigation: Remove the report or regenerate it with only style attributes before publishing, sharing, or installing in broader environments.

Risk: Untrusted DrawIO labels can be copied into AI-readable analysis reports.

Mitigation: Analyze trusted .drawio files only, or escape labels and treat them strictly as data before using generated reports.

Risk: Diagram parsing scripts process local XML and compressed DrawIO content.

Mitigation: Run the scripts in a resource-limited workspace when inspecting unfamiliar or large files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linlannet/skills/drawio-skills)
- [Publisher profile](https://clawhub.ai/user/linlannet)
- [Artifact README](artifact/README.md)
- [Linlan style preset](artifact/styles/linlan.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [DrawIO XML/.drawio files, Markdown analysis reports, JSON style presets, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional PNG, SVG, PDF, or JPG export depends on a local draw.io desktop CLI installation.]

## Skill Version(s):

1.0.0 (source: evidence release metadata, created 2026-09-12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
