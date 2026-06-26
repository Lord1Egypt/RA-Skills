## Description: <br>
Helps create FHIR-conformant Questionnaire definitions from plain requirements and supports LOINC and SNOMED CT lookup plus validation through local scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elmariachi111](https://clawhub.ai/user/elmariachi111) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, clinical informatics teams, and healthcare workflow builders use this skill to draft, code, and validate FHIR Questionnaire JSON from requirements. It is especially useful when questionnaires need terminology-backed LOINC or SNOMED CT codes and answer options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clinical terminology lookup terms may be sent to external terminology services. <br>
Mitigation: Do not include patient identifiers or sensitive clinical narratives in lookup terms; use minimal generic terms. <br>
Risk: Generated CodeSystem or ValueSet files may be created with unsuitable identifiers or in unintended locations. <br>
Mitigation: Use simple safe IDs, choose output directories deliberately, and review generated JSON before reuse. <br>
Risk: Questionnaire content may contain incorrect clinical codes if the lookup scripts are skipped or results are not checked. <br>
Mitigation: Use the official search and query scripts for LOINC and SNOMED CT codes, then validate Questionnaire JSON before finalizing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/elmariachi111/fhir-questionnaire) <br>
- [FHIR Questionnaire Reference Documentation](REFERENCE.md) <br>
- [FHIR Questionnaire Specification](references/fhir_questionnaire_spec.md) <br>
- [FHIR Questionnaire Spec](https://hl7.org/fhir/questionnaire.html) <br>
- [LOINC Coding Guide](references/loinc_guide.md) <br>
- [LOINC Database](https://loinc.org) <br>
- [SNOMED CT Guide](references/snomed_guide.md) <br>
- [FHIR Questionnaire Best Practices](references/best_practices.md) <br>
- [FHIR Questionnaire Examples](references/examples.md) <br>
- [Questionnaire JSON Schema](references/schema/questionnaire.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON FHIR resources and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local file paths for generated or validated Questionnaire, CodeSystem, and ValueSet JSON files.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
