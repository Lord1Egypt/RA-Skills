## Description:

CAD Editor helps agents turn natural-language drafting requests into CAD drawing code and deliverable engineering drawing files for architectural, mechanical, electrical, piping, structural, and general geometry workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and drafting-focused agents use this skill to generate CAD drawings from natural-language requests or direct Python API calls, including DXF creation, preview rendering, and PDF/SVG/PNG export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to execute generated Python from user-influenced drawing parameters.

Mitigation: Review generated code before execution and run it only in a sandboxed environment with no sensitive credentials or broad filesystem access.

Risk: User-provided filenames, output paths, or raw parameter dictionaries may affect generated outputs.

Mitigation: Constrain outputs to a dedicated directory and validate filenames, output paths, and drawing parameters before running generated code.

## Reference(s):

- [ACI color index](artifact/references/color_index.md)
- [DXF entity group codes](artifact/references/dxf_entity_codes.md)
- [Natural-language intent templates](artifact/references/intent_templates.json)
- [Layer standards](artifact/references/layer_standards.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files, guidance]

**Output Format:** [Markdown guidance with Python code blocks and generated DXF, PNG, SVG, or PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ezdxf, matplotlib, and numpy; generated drawing code should be reviewed and run in a sandboxed output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
