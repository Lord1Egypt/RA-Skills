## Description:

Compute HEIM diversity and equity metrics from VCF or ancestry data. Generates heterozygosity, FST, PCA plots, and a composite HEIM Equity Score with markdown reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manuelcorpas](https://clawhub.ai/user/manuelcorpas)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to analyze VCF or ancestry CSV data for genomic diversity, population representation, and HEIM equity scoring. It produces reports that help assess representation gaps before sharing or relying on study-level conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes persistent genomic and ancestry analysis reports that may contain sensitive dataset characteristics.

Mitigation: Run it in a restricted workspace with non-sensitive or approved data, and review generated reports before sharing.

Risk: Generated markdown includes reproducibility commands that may be copied or re-run later.

Mitigation: Review generated markdown and commands before executing or redistributing them.

Risk: HEIM scores and FST outputs can be mistaken for publication-ready conclusions.

Mitigation: Treat outputs as analytical aids and independently validate results before using them for research, publication, or operational decisions.

## Reference(s):

- [ClawBio repository](https://github.com/ClawBio/ClawBio)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with PNG figures, CSV tables, JSON score data, checksums, and reproducibility commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes persistent local analysis artifacts under an output directory.]

## Skill Version(s):

0.2.0 (source: ClawHub release evidence; artifact frontmatter lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
