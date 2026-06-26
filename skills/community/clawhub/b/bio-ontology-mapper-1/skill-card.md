## Description: <br>
Maps unstructured biomedical terms to standardized SNOMED CT and MeSH ontology concepts using local reference data and optional UMLS/MeSH API lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, biomedical data analysts, and informatics teams use this skill to normalize clinical or scientific terms into ontology identifiers for interoperability, search, and data harmonization workflows. It is not a substitute for clinical review or patient-care decision-making. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API mode can send submitted biomedical terms to external NLM services. <br>
Mitigation: Use local-only processing for confidential or patient-identifying data, and enable API lookup only after confirming text is de-identified and permitted by privacy and compliance requirements. <br>
Risk: Ontology mappings can be ambiguous, incomplete, or unsuitable for clinical decisions without expert review. <br>
Mitigation: Review low-confidence and high-impact mappings with qualified domain experts before using results in patient-care or regulated workflows. <br>
Risk: The listed Python requirements are unnecessary or unpinned. <br>
Mitigation: Avoid blindly installing the requirements file; inspect dependencies and use a controlled environment before execution. <br>


## Reference(s): <br>
- [Bio-Ontology Mapper release page](https://clawhub.ai/aipoch-ai/bio-ontology-mapper-1) <br>
- [UMLS API endpoint](https://uts-ws.nlm.nih.gov/rest) <br>
- [SNOMED sample reference data](references/snomed_sample.json) <br>
- [MeSH sample reference data](references/mesh_sample.json) <br>
- [Synonym reference data](references/synonyms.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown guidance with CLI commands; script results as JSON or plain text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write mapping results to an output file and can use external ontology APIs only when explicitly enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
