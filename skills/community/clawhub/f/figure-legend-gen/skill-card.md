## Description:

Generate standardized figure legends for scientific charts and graphs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, technical writers, and agents use this skill to draft standardized legends for scientific charts, graphs, and research images. It supports common figure types such as bar, line, scatter, box, heatmap, microscopy, flow cytometry, and western blot figures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner flags the release as suspicious because installation and file-writing behavior are under-scoped.

Mitigation: Review before installing; use an isolated virtual environment and a trusted package index, or remove unnecessary requirements.

Risk: The skill can write generated output to a user-specified path.

Mitigation: Keep --output inside the workspace and avoid overwriting existing files.

Risk: The documentation is unclear about claimed network/API behavior for unpublished or sensitive research figures.

Mitigation: Avoid running the skill on sensitive figures until the network/API behavior is reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/figure-legend-gen)
- [aipoch-ai publisher profile](https://clawhub.ai/user/aipoch-ai)
- [Figure Legend Templates](references/legend_templates.md)
- [Academic Figure Legend Style Guide](references/academic_style_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown, plain text, or LaTeX figure legend text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write generated legend text to stdout or to a user-specified output file.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
