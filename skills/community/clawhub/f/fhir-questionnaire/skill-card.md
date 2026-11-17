## Description:

Helps agents create FHIR-conforming Questionnaire definitions from requirement notes, with scripts for LOINC and SNOMED CT lookup and questionnaire validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elmariachi111](https://clawhub.ai/user/elmariachi111)

### License/Terms of Use:


## Use Case:

Developers and healthcare implementation teams use this skill to draft FHIR R4 Questionnaire JSON, identify terminology with official lookup scripts, choose answer options, and validate questionnaire structure before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Terminology lookups can send clinical search terms to remote terminology servers.

Mitigation: Keep lookups limited to trusted HTTPS FHIR terminology servers and avoid patient-identifying details in search terms.

Risk: Dependency installation is not pinned.

Mitigation: Review and pin dependencies before running setup.sh.

Risk: Incorrect clinical terminology could make generated questionnaires misleading.

Mitigation: Use only codes returned by the official lookup scripts and validate questionnaire JSON before finalizing.

## Reference(s):

- [Complete Documentation](REFERENCE.md)
- [FHIR Questionnaire Specification](references/fhir_questionnaire_spec.md)
- [HL7 FHIR Questionnaire](https://hl7.org/fhir/questionnaire.html)
- [LOINC Coding Guide](references/loinc_guide.md)
- [LOINC Database](https://loinc.org)
- [SNOMED CT Guide](references/snomed_guide.md)
- [FHIR Questionnaire Best Practices](references/best_practices.md)
- [FHIR Questionnaire Examples](references/examples.md)
- [Questionnaire JSON Schema](references/schema/questionnaire.schema.json)
- [ClawHub Skill Page](https://clawhub.ai/elmariachi111/skills/fhir-questionnaire)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate user-directed local FHIR Questionnaire, ValueSet, or CodeSystem JSON files.]

## Skill Version(s):

0.2.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
