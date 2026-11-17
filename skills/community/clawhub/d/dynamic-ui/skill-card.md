## Description:

Render tables, charts, stats, cards, and dashboards as images using HTML templates and wkhtmltoimage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theashbhat](https://clawhub.ai/user/theashbhat)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use Dynamic UI to turn structured JSON data into shareable PNG visualizations such as tables, KPI summaries, bar charts, cards, and dashboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rendering card images may cause network requests from wkhtmltoimage when user-provided image URLs are included.

Mitigation: Run the skill in an environment where wkhtmltoimage cannot reach sensitive internal services, and avoid rendering untrusted image URLs.

Risk: Rendered images can persist user-provided data on disk, including under ~/.openclaw/media or caller-selected output paths.

Mitigation: Avoid including secrets in rendered data and periodically clean media and output directories.

Risk: The security verdict is suspicious because the renderer has under-documented network and persistence behavior.

Mitigation: Review the skill before installing and scan it before deployment.

## Reference(s):

- [Dynamic UI ClawHub release](https://clawhub.ai/theashbhat/skills/dynamic-ui)
- [Publisher profile](https://clawhub.ai/user/theashbhat)
- [OpenClaw](https://openclaw.dev)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands; rendered skill output is PNG image files or base64 PNG text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports table, chart-bar, stats, card, and dashboard templates with modern, dark, and minimal themes.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
