## Description: <br>
Compute HEIM diversity and equity metrics from VCF or ancestry data. Generates heterozygosity, FST, PCA plots, and a composite HEIM Equity Score with markdown reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manuelcorpas](https://clawhub.ai/user/manuelcorpas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, bioinformaticians, and research teams use this skill to analyze VCF or ancestry CSV data for population representation, HEIM equity scores, heterozygosity, FST, PCA plots, and reproducible reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated genomic equity reports, figures, and tables may contain sensitive private information derived from VCF or ancestry data. <br>
Mitigation: Store output directories in private locations, avoid synced or shared folders for sensitive genomic outputs, and review reports before sharing. <br>
Risk: Analyzing VCF or ancestry CSV data without authorization could expose or misuse sensitive genomic information. <br>
Mitigation: Run the skill only on data you are authorized to analyze and keep processing local. <br>
Risk: Scientific outputs can vary if dependency versions change. <br>
Mitigation: Pin dependencies and retain generated reproducibility files, including commands, environment details, and checksums. <br>
Risk: Population labels can be mistaken for personal identity labels or overinterpreted. <br>
Mitigation: Treat ancestry categories as analytical groupings and include the report disclaimer that population labels are not identities. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/manuelcorpas/clawbio-equity-scorer) <br>
- [ClawBio project homepage](https://github.com/manuelcorpas/ClawBio) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, analysis, files] <br>
**Output Format:** [Markdown reports with PNG figures, CSV tables, JSON score data, and reproducibility files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally on user-provided genomic or ancestry data and writes outputs to an equity_report directory by default.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
