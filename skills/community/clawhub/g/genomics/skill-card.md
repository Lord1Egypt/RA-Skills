## Description: <br>
Interpret genomic variants with ACMG classification, pharmacogenomics, and clinical annotation from ClinVar and gnomAD. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External clinicians, geneticists, bioinformaticians, and researchers use this skill to interpret processed genomic variants from VCF-style workflows. It supports evidence-based ACMG classification, pharmacogenomics interpretation, clinical annotation lookup, and clear separation of germline and somatic context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Genomic interpretation can involve sensitive health information and may produce clinical or pharmacogenomics recommendations that require professional verification. <br>
Mitigation: Avoid saving patient identifiers unless necessary, review local notes under ~/genomics/ periodically, and independently verify clinical or pharmacogenomics recommendations against current professional guidance. <br>
Risk: The skill can store interpretation preferences and case notes locally after user consent. <br>
Mitigation: Confirm consent before creating ~/genomics/ and keep stored notes limited to the minimum information needed for the user's workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/genomics) <br>
- [Skill Homepage](https://clawic.com/skills/genomics) <br>
- [ClinVar](https://www.ncbi.nlm.nih.gov/clinvar) <br>
- [gnomAD](https://gnomad.broadinstitute.org) <br>
- [OMIM](https://omim.org) <br>
- [PharmGKB](https://www.pharmgkb.org) <br>
- [CPIC](https://cpicpgx.org) <br>
- [ClinGen](https://clinicalgenome.org) <br>
- [Franklin](https://franklin.genoox.com) <br>
- [VarSome](https://varsome.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance with optional local workspace notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local notes under ~/genomics/ only with user consent; does not automatically call external APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
