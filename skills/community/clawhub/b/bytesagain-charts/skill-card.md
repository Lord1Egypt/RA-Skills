## Description:

Generate ASCII, HTML, and SVG charts from CSV, JSON, or inline data for quick data visualization workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent users use this skill to turn simple datasets into terminal charts, HTML charts, SVG files, tables, dashboards, and visualization guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe HTML or SVG can be generated when untrusted chart labels or titles are provided.

Mitigation: Use only trusted chart data and review generated HTML or SVG before opening, publishing, or sharing it.

Risk: Chart files and a local history log may be left on disk.

Mitigation: Run the skill in a workspace intended for generated artifacts and remove local chart outputs or history after use when data is sensitive.

Risk: Some advertised chart features may not behave as documented.

Mitigation: Test required chart commands with representative data before relying on the output in reports or automation.

## Reference(s):

- [BytesAgain homepage](https://bytesagain.com)
- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/bytesagain-charts)
- [Publisher profile](https://clawhub.ai/user/xueyetianya)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with shell command examples and generated chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce terminal output plus local HTML, SVG, and history files depending on the invoked chart command.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
