## Description:

Detect copy number variations from whole genome sequencing data and generate publication-quality genome-wide CNV plots.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and bioinformatics analysts use this skill to draft CNV calling and visualization workflows for whole genome sequencing data. Current outputs should be treated as demonstration data until the CNV algorithm and validation are completed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The current implementation can present hard-coded CNV results as analysis output.

Mitigation: Use only demonstration data until the CNV algorithm, plotting behavior, and output validation are implemented and independently validated.

Risk: Genomic inputs may include patient-related or otherwise sensitive data.

Mitigation: Process only approved, de-identified data in controlled environments that meet applicable privacy and compliance requirements.

Risk: Unvalidated CNV output could affect research, clinical, publication, or patient-related decisions.

Mitigation: Require expert review and validated clinical or research pipelines before using any result for decision-making.

Risk: Input validation, dependency specification, and privacy handling are not proven by the evidence.

Mitigation: Review the skill, test it with non-sensitive fixtures, and define runtime dependencies and data-handling controls before installation or use.

## Reference(s):

- [Cnv Caller Plotter on ClawHub](https://clawhub.ai/aipoch-ai/skills/cnv-caller-plotter)
- [Database of Genomic Variants](http://dgv.tcag.ca)
- [gnomAD Structural Variants](https://gnomad.broadinstitute.org)
- [ClinVar](https://www.ncbi.nlm.nih.gov/clinvar)
- [DECIPHER](https://www.deciphergenomics.org)
- [COSMIC](https://cancer.sanger.ac.uk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with Python and shell examples; script output may include BED files and plot file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Demonstration implementation returns fixed CNV examples and writes BED output when executed.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
