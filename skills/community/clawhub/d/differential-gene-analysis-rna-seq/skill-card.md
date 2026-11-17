## Description:

Performs differential gene expression analysis on RNA-seq count data using DESeq2, generating significant gene lists and visualizations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenthompson2088](https://clawhub.ai/user/kenthompson2088)

### License/Terms of Use:

MIT-0

## Use Case:

Bioinformatics practitioners and data analysts use this skill to run a DESeq2-based RNA-seq differential expression workflow and generate plots plus a significant-gene results table from a count matrix.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow installs unpinned R and Bioconductor packages at runtime, which can affect reproducibility and supply-chain control.

Mitigation: Run it in a sandboxed R environment, preinstall dependencies from trusted repositories, and use pinned package versions or an renv lockfile for reproducible work.

Risk: The evidence notes an empty input file and a missing main.R packaging mismatch, so the skill may not run as packaged.

Mitigation: Resolve the packaged input and entry-file mismatch before using the skill with private or production RNA-seq data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kenthompson2088/skills/differential-gene-analysis-rna-seq)

## Skill Output:

**Output Type(s):** [Analysis, Files]

**Output Format:** [CSV and PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a significant differential genes CSV file plus volcano, PCA, and heatmap visualizations.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
