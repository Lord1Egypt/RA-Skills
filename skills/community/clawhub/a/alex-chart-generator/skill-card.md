## Description:

Data visualization tool producing SVG charts, ASCII charts, tables, sparklines, gauges, and other visualizations from raw numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shendingyi](https://clawhub.ai/user/shendingyi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and other external users can use this skill to generate quick terminal charts, SVG or HTML chart files, tables, sparklines, dashboards, and visualization guidance from simple numeric inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SVG or HTML can include unescaped user-provided labels or titles.

Mitigation: Treat generated SVG/HTML as active content and avoid opening or hosting charts built from untrusted input in a trusted browser context.

Risk: The packaged secondary script can retain local chart history under the user data directory.

Mitigation: Avoid charting sensitive data unless local history behavior is acceptable, and review or clear the chart-generator data directory when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shendingyi/skills/alex-chart-generator)
- [Data visualization best practices](artifact/tips.md)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Guidance]

**Output Format:** [Plain text charts, Markdown guidance, and SVG or HTML chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated SVG and HTML may include user-supplied chart labels or titles; one packaged script can retain local chart history under the user data directory.]

## Skill Version(s):

2.3.4 (source: server release metadata and artifact/_meta.json; artifact/SKILL.md frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
