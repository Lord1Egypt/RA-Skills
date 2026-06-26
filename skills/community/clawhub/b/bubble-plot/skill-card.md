## Description: <br>
Generates gene-expression bubble (dot) plots for TSV or CSV datasets, showing expression percentage and average expression by cell type and cancer type. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fmaxy](https://clawhub.ai/user/fmaxy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, developers, and data analysts use this skill to visualize gene expression patterns in single-cell RNA-seq, spatial transcriptomics, or similar expression datasets. It helps create bubble plots grouped by cell type and cancer type, optionally filtered to selected genes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may be triggered for generic chart requests rather than gene-expression bubble plots. <br>
Mitigation: Use it only when the user requests bubble or dot plots for TSV/CSV gene-expression data and confirms the dataset structure. <br>
Risk: The skill's setup guidance may install pandas and matplotlib system-wide. <br>
Mitigation: Prefer a virtual environment or project-local environment before installing dependencies. <br>
Risk: Plot files are written to a local output directory. <br>
Mitigation: Choose the output directory intentionally and review generated PNG and PDF files before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fmaxy/bubble-plot) <br>
- [Publisher profile](https://clawhub.ai/user/fmaxy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated plot files are PNG and PDF.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script writes one PNG and one PDF per gene and tissue grouping, reports generated file paths and sizes, and may preview selected plots.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
