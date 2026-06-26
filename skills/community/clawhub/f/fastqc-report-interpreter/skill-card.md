## Description: <br>
Use when analyzing FASTQC quality reports from sequencing data, identifying quality issues in NGS datasets, or troubleshooting sequencing problems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, bioinformatics analysts, and sequencing workflow maintainers use this skill to interpret FastQC quality reports, identify common NGS quality issues, and get actionable recommendations for RNA-seq, DNA-seq, and ChIP-seq data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad local agent tools for reading, writing, shell execution, and editing. <br>
Mitigation: Use it only on intended FastQC report files and review proposed shell commands or file writes before allowing them. <br>
Risk: Packaged script names and documented examples do not fully match, so some usage examples may fail without adjustment. <br>
Mitigation: Check the packaged file paths and command names before running examples in an analysis workflow. <br>
Risk: Quality interpretation is simplified and may not capture every sequencing platform or library-preparation context. <br>
Mitigation: Treat recommendations as decision support and confirm important QC decisions against project-specific thresholds and downstream analysis requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AIPOCH-AI/fastqc-report-interpreter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize FastQC module status, quality issues, and recommended remediation steps.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
