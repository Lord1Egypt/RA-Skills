## Description: <br>
Detect copy number variations from whole genome sequencing data and generate publication-quality genome-wide CNV plots. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and bioinformatics analysts can use this skill as a reviewable demonstration for CNV calling workflows, genome-wide CNV visualization, and BED-style CNV output planning. It should not be relied on for research, publication, medical, diagnostic, or patient-related decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill presents placeholder genomics behavior as if it were a working CNV analysis tool. <br>
Mitigation: Treat outputs as demonstration material only and require validated CNV pipelines for research, publication, medical, diagnostic, or patient-related decisions. <br>
Risk: The workflow may process sensitive genomic input and output files. <br>
Mitigation: Handle BAM, VCF, BED, plots, and related outputs only in approved secure environments with appropriate data governance. <br>
Risk: CNV calls and plots can be misleading if used without quality review, matched controls, or orthogonal validation. <br>
Mitigation: Require expert review, quality checks, and independent validation before any scientific or clinical interpretation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AIPOCH-AI/cnv-caller-plotter) <br>
- [Database of Genomic Variants](http://dgv.tcag.ca) <br>
- [gnomAD](https://gnomad.broadinstitute.org) <br>
- [ClinVar](https://www.ncbi.nlm.nih.gov/clinvar) <br>
- [DECIPHER](https://www.deciphergenomics.org) <br>
- [COSMIC Cancer Gene Census](https://cancer.sanger.ac.uk) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Files] <br>
**Output Format:** [Markdown with Python and bash code blocks; generated file examples include BED calls and plot paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference sensitive genomic input and output files that require approved secure handling.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
