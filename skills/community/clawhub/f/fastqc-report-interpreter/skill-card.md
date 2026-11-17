## Description:

Use when analyzing FASTQC quality reports from sequencing data, identifying quality issues in NGS datasets, or troubleshooting sequencing problems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and bioinformatics analysts use this skill to interpret FastQC quality reports, flag common NGS sequencing quality issues, and generate recommendations before downstream RNA-seq, DNA-seq, or ChIP-seq analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some documentation examples reference filenames or command options that are not present in the package.

Mitigation: Verify the included script path and supported arguments before automating the skill; use the packaged script interface when examples differ.

Risk: FastQC interpretation is heuristic and may not capture every assay-specific quality concern.

Mitigation: Review recommendations against the raw FastQC report, sequencing assay expectations, and local analysis procedures before changing downstream workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/fastqc-report-interpreter)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with Python and bash examples plus plain-text analysis and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize FastQC module status, quality concerns, and suggested next actions.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact metadata reports 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
