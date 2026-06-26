## Description: <br>
Map unstructured biomedical text to standardized ontologies (SNOMED CT, MeSH, ICD-10) for terminology normalization and semantic interoperability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renhaosu2024](https://clawhub.ai/user/renhaosu2024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, biomedical informatics teams, and data engineers use this skill to normalize clinical or scientific free text into ontology-backed terms, codes, and confidence scores for EHR integration, study harmonization, literature indexing, and data warehouse preparation. It is not a substitute for clinical diagnosis, real-time patient care, or expert coding review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clinical notes or study data may contain PHI, and API mode can send terms to external NLM ontology services. <br>
Mitigation: De-identify sensitive text before use and disable API mode when policy requires local-only processing. <br>
Risk: Low-confidence or ambiguous ontology mappings can be incorrect for high-stakes biomedical workflows. <br>
Mitigation: Review low-confidence mappings and clinically important outputs with a qualified domain expert before downstream use. <br>
Risk: The local Python mapper can read input files and write output files. <br>
Mitigation: Run it in an appropriate workspace with reviewed input and output paths. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/renhaosu2024/bio-ontology-mapper) <br>
- [UMLS UTS API](https://uts-ws.nlm.nih.gov/rest) <br>
- [SNOMED sample reference data](artifact/references/snomed_sample.json) <br>
- [MeSH sample reference data](artifact/references/mesh_sample.json) <br>
- [Synonym reference data](artifact/references/synonyms.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell examples; mapper runtime output is JSON or plain text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Mapping outputs include input terms, ontology names, concept identifiers, preferred terms, confidence scores, source indicators, optional synonyms or tree numbers, and API status.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
