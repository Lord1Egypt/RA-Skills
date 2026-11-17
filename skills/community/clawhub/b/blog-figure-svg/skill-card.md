## Description:

Generates accessible, lightweight SVG figures and rasterized PNGs for blog posts and CMS publishing workflows, including flow diagrams, comparison charts, taxonomy diagrams, terminal mocks, and 1600x840 feature cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[automatelab](https://clawhub.ai/user/automatelab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content marketers, indie publishers, and dev-tool blog teams use this skill to create editorial figures and feature images after article prose is stable. It supports CMS and static-site publishing workflows that need accessible SVG source plus compressed PNG output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes generated image files into a working directory and depends on local rasterizer and compressor tooling.

Mitigation: Install only for editorial SVG/PNG generation workflows, use a virtual environment or managed rasterizer, and prefer pinned dependencies.

Risk: Unexpected color or accent inputs can weaken consistency or produce invalid figure output.

Mitigation: Keep accent and color inputs to known hex values from the documented palette.

Risk: Generated charts or diagrams can mislead readers if they plot data not present in the article or exaggerate differences.

Mitigation: Review generated figures against the article source data and retain the documented rule to avoid plotting unsupported data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/automatelab/skills/blog-figure-svg)
- [Publisher profile](https://clawhub.ai/user/automatelab)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with SVG, HTML, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces editable SVG source and compressed PNG image outputs in the working directory.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
