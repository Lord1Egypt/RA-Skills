## Description: <br>
Generates a pharmacogenomic Markdown report from 23andMe or AncestryDNA raw genetic data. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[manuelcorpas](https://clawhub.ai/user/manuelcorpas) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and bioinformatics users can use this skill to process local DTC genetic data and generate a structured pharmacogenomic report with gene profiles, drug-response recommendations, and safety alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes sensitive genetic data and writes a report that may contain private health-related information. <br>
Mitigation: Run it locally with private input and output paths, avoid shared or synced folders unless appropriate, and delete generated reports when no longer needed. <br>
Risk: The report includes medication guidance derived from DTC genetic data and is not a diagnostic device. <br>
Mitigation: Do not make medication or dose decisions from the report without a qualified healthcare professional and confirmatory clinical-grade testing. <br>


## Reference(s): <br>
- [ClawBio project homepage](https://github.com/manuelcorpas/ClawBio) <br>
- [PharmGx Reporter on ClawHub](https://clawhub.ai/manuelcorpas/clawbio-pharmgx-reporter) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, guidance] <br>
**Output Format:** [Markdown report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes gene profiles, drug recommendation tables, actionable alerts, input checksum, and reproducibility command.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
