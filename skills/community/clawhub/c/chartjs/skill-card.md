## Description:

Chart.js charting skill. Used to generate visual charts such as line charts, bar charts, pie charts, radar charts, scatter plots, etc.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create Chart.js visualizations from provided data, including line, bar, pie, radar, scatter, bubble, doughnut, and polar area charts. It supports generating chart code, HTML rendering guidance, and screenshot or image export workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npm or CDN dependencies can change behavior over time or introduce supply-chain exposure.

Mitigation: Use pinned Chart.js package versions, lockfiles, and versioned CDN URLs with integrity hashes.

Risk: Generated HTML, image, or PDF files may be written to an unexpected location.

Mitigation: Confirm output paths before writing or exporting generated chart artifacts.

## Reference(s):

- [Chart.js API Reference](references/api.md)
- [ClawHub skill page](https://clawhub.ai/openlark/skills/chartjs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline HTML, JavaScript, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce complete HTML files for browser rendering or guidance for screenshot, image, and PDF export.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
