## Description: <br>
Compute HEIM diversity and equity metrics from VCF or ancestry data, generating heterozygosity, FST, PCA plots, and a composite HEIM Equity Score with markdown reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manuelcorpas](https://clawhub.ai/user/manuelcorpas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Bioinformatics practitioners and researchers use this skill to assess representation and diversity in VCF genotype data or ancestry tables, then produce HEIM equity reports with figures and reproducibility details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CSV-only analyses can present estimated genetic metrics as if they were computed from genotype data. <br>
Mitigation: Use VCF input when genotype-derived heterozygosity, FST, and PCA are required, and label CSV-only HEIM scores as estimates before sharing reports. <br>
Risk: Genomic and ancestry data can be sensitive personal data. <br>
Mitigation: Run the skill only on data you are authorized to analyze, keep generated reports in a private local directory, and review outputs before distribution. <br>


## Reference(s): <br>
- [ClawBio homepage](https://github.com/ClawBio/ClawBio) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, CSV tables, JSON score files, PNG figures, and reproducibility commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally on authorized VCF or ancestry CSV inputs and writes results to an output directory.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata; artifact frontmatter lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
