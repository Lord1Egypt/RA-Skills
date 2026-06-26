## Description: <br>
Performs differential gene expression analysis on RNA-seq count data using DESeq2, generating significant gene lists and visualizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenthompson2088](https://clawhub.ai/user/kenthompson2088) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and bioinformatics analysts use this skill to run a DESeq2-based RNA-seq differential expression workflow from a count matrix and produce plots plus a significant-gene table. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may contact CRAN or Bioconductor and modify the local R package library before analysis. <br>
Mitigation: Review the package installation lines first and run in a locked, isolated, or offline R environment when dependency changes are not acceptable. <br>
Risk: The workflow depends on a valid RNA-seq count matrix at input/count_matrix.csv. <br>
Mitigation: Provide and review the count matrix before running so outputs are based on the intended samples and groups. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kenthompson2088/differential-gene-analysis-rna-seq) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Analysis] <br>
**Output Format:** [R-generated CSV and PNG files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces volcano.png, pca.png, heatmap.png, and diff_genes_significant.csv under output/.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
