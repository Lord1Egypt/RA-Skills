## Description: <br>
Performs differential gene expression analysis on RNA-seq count data using DESeq2 and outputs significant genes, volcano plot, PCA plot, and heatmap. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenthompson2088](https://clawhub.ai/user/kenthompson2088) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Bioinformatics analysts and developers use this skill to run DESeq2 differential expression analysis on RNA-seq count matrices and generate significant-gene tables and exploratory plots. The artifact uses Control versus Treat group assignments for the analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads input/count_matrix.csv, which may contain sensitive RNA-seq count data. <br>
Mitigation: Use only data approved for local processing and avoid placing sensitive count data in the input path unless that processing is acceptable. <br>
Risk: The skill may download and install R and Bioconductor packages if required packages are not already present. <br>
Mitigation: Run it in a project-specific or disposable R environment when package changes matter. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kenthompson2088/differential-gene-analysis) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/kenthompson2088) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Analysis] <br>
**Output Format:** [PNG plots and CSV results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes volcano.png, pca.png, heatmap.png, and diff_genes_significant.csv under the output directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
