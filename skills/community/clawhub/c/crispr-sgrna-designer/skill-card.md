## Description:

CRISPR sgRNA Designer helps agents propose and rank SpCas9 sgRNA candidates for viral and microbial genomes, including high-GC templates, using PAM scanning and heuristic scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zjuphd](https://clawhub.ai/user/zjuphd)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, bioinformatics practitioners, and researchers use this skill to generate preliminary sgRNA candidate lists, ranking summaries, and donor-template editing considerations for viral or microbial genome targets. Outputs should be reviewed with independent CRISPR and off-target analysis tools before experimental use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may overstate safety-critical CRISPR design confidence and should not be treated as validated low-off-target or precise-edit guidance.

Mitigation: Treat outputs as preliminary candidates and use independent CRISPR/off-target tools plus expert review before experimental use.

Risk: Accession-based lookup may send target accession and coordinate details to NCBI E-utilities.

Mitigation: Avoid external lookup for sensitive or proprietary targets unless that disclosure is acceptable; provide local sequence input instead.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zjuphd/skills/crispr-sgrna-designer)
- [NCBI E-utilities EFetch endpoint used by the helper script](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with optional JSON candidate output from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May contact NCBI E-utilities when accession-based sequence lookup is used.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
