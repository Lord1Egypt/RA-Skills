## Description:

Generate Circos configuration files for circular genomics data visualization, including genomic variations, cell-cell communication networks, and custom track configurations for publication-ready circular plots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renhaosu2024](https://clawhub.ai/user/renhaosu2024)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, bioinformatics practitioners, and developers use this skill to prepare Circos configuration and supporting data files for circular genomics visualizations, including variant, structural rearrangement, and cell-cell communication plots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags an ambiguous YAML dependency and dependency-review gap.

Mitigation: Replace the ambiguous yaml requirement with the intended reviewed, pinned YAML library before installation.

Risk: The skill reads user-supplied CSV/YAML inputs and writes generated configuration files.

Mitigation: Use trusted inputs, choose a fresh output directory, and avoid elevated privileges when generating files.

Risk: Optional Circos rendering runs a local external command against generated configuration.

Mitigation: Run rendering in a constrained working directory and review generated configuration before rendering.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/renhaosu2024/skills/circos-plot-generator)
- [Circos Documentation](http://circos.ca/documentation)
- [Circos Tutorials](http://circos.ca/documentation/tutorials)
- [Bioconda Circos Recipe](https://bioconda.github.io/recipes/circos/README.html)

## Skill Output:

**Output Type(s):** [configuration, code, shell commands, guidance]

**Output Format:** [Markdown guidance with Python and shell examples; generated Circos configuration and data files when executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May optionally invoke local Circos rendering when the user requests it and Circos is installed.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
