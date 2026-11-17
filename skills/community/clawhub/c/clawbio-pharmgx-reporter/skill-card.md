## Description:

Generates pharmacogenomic reports from DTC genetic data from 23andMe or AncestryDNA.

This skill is for research and development only.

## Publisher:

[manuelcorpas](https://clawhub.ai/user/manuelcorpas)

### License/Terms of Use:

MIT

## Use Case:

Developers and bioinformatics users use this skill to process raw consumer genotype files and generate educational pharmacogenomic markdown reports with gene profiles, drug-response tables, and alerts. The reports are not clinical advice and should not be used for medication decisions without healthcare-professional review and confirmatory testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports can contain actionable medication recommendations based on consumer genetic data.

Mitigation: Use reports only for education and review any medication-related interpretation with a qualified healthcare professional and confirmatory clinical-grade testing.

Risk: Input files and generated reports contain sensitive genetic health information.

Mitigation: Process files locally, restrict access to outputs, and store or delete generated reports according to sensitive health-record handling expectations.

Risk: Report integrity may be affected by untrusted files or filenames while markdown escaping and genotype validation remain areas for review.

Mitigation: Use trusted local input files and review generated markdown before sharing or relying on the report.

## Reference(s):

- [ClawBio GitHub Homepage](https://github.com/manuelcorpas/ClawBio)
- [CPIC](https://cpicpgx.org/)
- [PharmGKB](https://www.pharmgkb.org/)
- [ClawHub Skill Page](https://clawhub.ai/manuelcorpas/skills/clawbio-pharmgx-reporter)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown report with command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates local report files from a user-provided raw genotype file; reports may contain sensitive genetic health information.]

## Skill Version(s):

0.1.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
