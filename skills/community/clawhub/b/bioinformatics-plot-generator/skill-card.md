## Description:

Route to the correct publication-quality plot sub-skill for volcano plots, heatmaps, box/violin plots, scatter plots, bar charts, MA plots, correlation matrices, and bubble charts from bioinformatics data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xutaoguo55](https://clawhub.ai/user/xutaoguo55)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route bioinformatics plotting requests to the correct sub-skill for tabular or matrix data. It supports static, publication-quality figures and optional analysis tables for common genomics, proteomics, and clinical data visualization workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scripts import missing shared plotting code from outside the reviewed artifact.

Mitigation: Fix or bundle _shared/plot_style.py before installation, and review any parent-directory code that could be imported by the plotting scripts.

Risk: The skill may be run on sensitive clinical or genomic datasets while the packaging issue remains unresolved.

Mitigation: Use an isolated environment with reviewed dependencies and avoid private clinical or genomic data until the missing shared-code dependency is resolved.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, files, text]

**Output Format:** [Markdown guidance with inline shell commands and generated PNG, SVG, PDF, or TSV file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primary artifacts are static publication-quality plots; some sub-skills can also emit annotated or processed TSV tables and console summaries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
