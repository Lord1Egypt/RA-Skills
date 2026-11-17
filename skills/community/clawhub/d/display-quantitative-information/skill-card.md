## Description:

Helps agents design, critique, redesign, audit, generate, code, and explain quantitative displays while checking graphical integrity, accessibility, and misleading encodings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tristanmanchester](https://clawhub.ai/user/tristanmanchester)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and other external users use this skill to choose, audit, redesign, and generate evidence-focused quantitative displays such as charts, dashboards, tables, maps, and scientific figures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read user-provided data files during chart critique, display selection, and rendering tasks.

Mitigation: Use it with data the user intends the agent to read, and avoid very large or untrusted CSV files until input limits are added.

Risk: Chart rendering can overwrite files when an output path is reused.

Mitigation: Choose output paths deliberately and confirm existing files before writing chart artifacts.

Risk: Generated chart recommendations or SVG outputs may omit important context for decision-making.

Mitigation: Review generated displays for source, units, uncertainty, denominators, and accessibility before relying on them in reports or slides.

## Reference(s):

- [Principles](references/principles.md)
- [Display Selection](references/display-selection.md)
- [Integrity Audit](references/integrity-audit.md)
- [Redesign Workflow](references/redesign-workflow.md)
- [Chart Specification](references/chart-spec.md)
- [Accessibility and Output](references/accessibility-and-output.md)
- [Language and Variation](references/language-and-variation.md)
- [Rubric](references/rubric.md)
- [Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional code blocks, JSON chart specifications, shell commands, and SVG chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write chart files to user-selected output paths when rendering SVGs.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
