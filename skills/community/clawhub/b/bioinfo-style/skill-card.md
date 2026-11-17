## Description:

Guides agents through reproducible bioinformatics workflows for sequencing quality control, alignment, quantification, differential analysis, enrichment analysis, and visualization using established tools and R Markdown reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biociao](https://clawhub.ai/user/biociao)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, bioinformatics analysts, and research teams use this skill to plan and script reproducible sequencing analysis workflows, including RNA-seq, ChIP-seq, WGS, differential expression, enrichment analysis, and omics visualization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead agents to install Conda or Mamba packages and execute local analysis scripts.

Mitigation: Review generated scripts and environment changes before execution, and use the skill only in project directories where generated scripts, logs, and package changes are acceptable.

Risk: The bundled helper script can write logs outside the intended directory when given unsafe step names.

Mitigation: Use controlled step names or harden scripts/run_step.sh before relying on it in shared or sensitive workspaces.

## Reference(s):

- [Analysis script templates](references/templates.md)
- [Bioinformatics tools quick reference](references/tools.md)
- [ClawHub skill page](https://clawhub.ai/biociao/skills/bioinfo-style)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with bash, R Markdown, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include project directory layouts, Conda or Mamba environment commands, analysis scripts, logs guidance, and report templates.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
