## Description:

Performs differential gene expression analysis on RNA-seq count data using DESeq2 and outputs significant genes, a volcano plot, PCA plot, and heatmap.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenthompson2088](https://clawhub.ai/user/kenthompson2088)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, bioinformaticians, and data analysts use this skill to run a DESeq2-based RNA-seq differential expression workflow that produces tabular significant-gene results and common exploratory visualizations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs unpinned CRAN and Bioconductor packages at runtime, which can affect reproducibility and supply-chain control.

Mitigation: Run it in a contained R environment and review or pin package versions before relying on results.

Risk: The bundled input CSV is empty, so the workflow will not succeed without valid RNA-seq count data.

Mitigation: Provide a populated count matrix before execution and confirm that sample columns match the expected analysis design.

Risk: The analysis code uses fixed Control and Treat group assignments for six samples.

Mitigation: Review and adjust the group labels to match the supplied experiment before interpreting differential expression results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kenthompson2088/skills/differential-gene-analysis)
- [Publisher profile](https://clawhub.ai/user/kenthompson2088)

## Skill Output:

**Output Type(s):** [Files, Analysis]

**Output Format:** [PNG visualizations and CSV results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces volcano.png, pca.png, heatmap.png, and diff_genes_significant.csv in an output directory when valid count data is supplied.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
