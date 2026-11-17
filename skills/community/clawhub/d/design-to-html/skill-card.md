## Description:

Converts visual design mockups or screenshots into HTML/CSS and iteratively refines the output with visual comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nodermachine](https://clawhub.ai/user/nodermachine)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and design engineers use this skill to convert static visual designs into HTML/CSS, inspect pixel-level differences, and produce comparison reports for refinement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML is rendered in a browser environment that the security evidence describes as under-contained.

Mitigation: Render only reviewed inputs in an isolated environment, avoid network access while rendering, and keep browser execution sandboxed from sensitive files and credentials.

Risk: The Python pipeline can install an unpinned package at runtime, which may modify the active Python environment.

Mitigation: Pin dependencies in a lockfile or controlled environment and remove or gate automatic pip install behavior before routine use.

Risk: The provided security verdict is suspicious and recommends review before installing.

Mitigation: Review the skill before installation, run it in an isolated workspace, and follow the provided security guidance for dependency pinning and HTML rendering.

## Reference(s):

- [Design To Html ClawHub Skill Page](https://clawhub.ai/nodermachine/skills/design-to-html)
- [Button Component Example](references/examples/button-example.md)
- [Card Component Example](references/examples/card-example.md)

## Skill Output:

**Output Type(s):** [Code, Markdown, JSON, Shell commands, Files, Guidance]

**Output Format:** [HTML/CSS, Markdown reports, JSON metrics, PNG screenshots, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include final.html, comparison_report.md, rendered and diff PNGs, and per-iteration files.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
