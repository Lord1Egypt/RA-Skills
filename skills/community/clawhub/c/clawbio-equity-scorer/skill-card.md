## Description:

Compute HEIM diversity and equity metrics from VCF or ancestry data. Generates heterozygosity, FST, PCA plots, and a composite HEIM Equity Score with markdown reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manuelcorpas](https://clawhub.ai/user/manuelcorpas)

### License/Terms of Use:


## Use Case:

External developers and bioinformatics researchers use this skill to assess population diversity and representation equity in genomic cohorts from VCF or ancestry CSV inputs. It helps produce HEIM scores, visualizations, summary tables, and reproducibility materials for local review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce sensitive genomic and ancestry reports as persistent local files.

Mitigation: Use a private output directory and avoid running the analysis on shared machines for sensitive datasets.

Risk: Inferred population labels or CSV-only HEIM scores can be misleading.

Mitigation: Provide an explicit reviewed population map and treat CSV-only scores as limited summaries.

Risk: Generated CSV or Markdown may contain untrusted labels that become unsafe when opened in spreadsheet or rich-content tools.

Mitigation: Open generated files with formulas and remote content disabled when labels come from untrusted data.

## Reference(s):

- [ClawBio GitHub repository](https://github.com/manuelcorpas/ClawBio)
- [ClawHub skill page](https://clawhub.ai/manuelcorpas/skills/clawbio-equity-scorer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with CSV tables, JSON score data, PNG figures, and reproducibility files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are written locally, normally under an equity_report directory.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
