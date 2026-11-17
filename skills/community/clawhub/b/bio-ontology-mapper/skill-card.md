## Description:

Map unstructured biomedical text to standardized ontologies such as SNOMED CT, MeSH, and ICD-10 for terminology normalization and semantic interoperability, with entity extraction and confidence scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renhaosu2024](https://clawhub.ai/user/renhaosu2024)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and biomedical informatics teams use this skill to normalize free-text clinical or scientific terms into ontology identifiers for EHR integration, research datasets, literature indexing, and data harmonization. Outputs should be reviewed by domain experts before use in clinical or high-stakes workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive clinical terms and an API key can be sent to external services in URL query strings when API mode is used.

Mitigation: Use local-only mode for clinical or identifiable data, de-identify inputs before external lookup, and avoid passing API keys on the command line.

Risk: The release evidence says the skill overstates capabilities, including advertised ICD-10, NER, and cross-mapping features.

Mitigation: Treat those capabilities as unimplemented unless the package is corrected, and validate outputs against domain expertise or gold-standard data before relying on them.

Risk: The authoritative security verdict is suspicious because of privacy and install concerns, even though the evidence does not show malicious behavior, persistence, or hidden exfiltration.

Mitigation: Review before installing, scan the artifact in the target environment, and restrict use to reviewed workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/renhaosu2024/skills/bio-ontology-mapper)
- [UMLS UTS API](https://uts-ws.nlm.nih.gov/rest)
- [MeSH API](https://id.nlm.nih.gov/mesh)
- [SNOMED sample reference](artifact/references/snomed_sample.json)
- [MeSH sample reference](artifact/references/mesh_sample.json)
- [Synonyms reference](artifact/references/synonyms.json)

## Skill Output:

**Output Type(s):** [text, json, files, shell commands, guidance]

**Output Format:** [Markdown guidance with inline Python and shell examples; CLI results are JSON or plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read terms from a file and optionally write mapping results to an output file.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
