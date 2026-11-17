## Description:

Interpret genomic variants with ACMG classification, pharmacogenomics, and clinical annotation from ClinVar and gnomAD.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Clinicians, geneticists, bioinformaticians, and researchers use this skill to interpret processed genomic variants, classify clinical significance, annotate variants against reference databases, and prepare pharmacogenomics guidance. It is not intended for raw sequencing alignment, variant calling, or standalone medical decision-making.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Genomic and clinical case notes can contain identifying or sensitive health information.

Mitigation: Create the ~/genomics/ workspace only with user consent and avoid storing patient identifiers unless appropriate privacy controls are in place.

Risk: Variant classifications, pharmacogenomics recommendations, and dosing guidance may be incorrect, incomplete, or out of date.

Mitigation: Verify interpretations against current clinical guidelines, trusted databases, and qualified professional review before using them in clinical decisions.

Risk: Manual lookup on external databases may expose variant or case context if the user submits sensitive data.

Mitigation: Use external resources deliberately and minimize any sensitive data entered into third-party sites.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/genomics)
- [Skill homepage](https://clawic.com/skills/genomics)
- [ClinVar](https://ncbi.nlm.nih.gov/clinvar)
- [gnomAD](https://gnomad.broadinstitute.org)
- [OMIM](https://omim.org)
- [PharmGKB](https://pharmgkb.org)
- [CPIC](https://cpicpgx.org)
- [ClinGen](https://clinicalgenome.org)
- [Franklin](https://franklin.genoox.com)
- [VarSome](https://varsome.com)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with optional local notes and case summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local notes under ~/genomics/ only after user consent; no automatic network calls or code execution are disclosed.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
