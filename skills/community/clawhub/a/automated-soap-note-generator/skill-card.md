## Description: <br>
Transforms unstructured clinical input, dictation, transcripts, or rough notes into standardized SOAP medical documentation for physician-reviewed draft generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Healthcare documentation users and clinical workflow developers use this skill to convert physician dictation, transcripts, or rough encounter notes into draft SOAP notes for licensed clinician review before patient-record use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can save sensitive patient information locally. <br>
Mitigation: Use only in a HIPAA-compliant or otherwise approved clinical environment, avoid protected health information in unsecured paths, and choose protected output locations. <br>
Risk: Generated SOAP notes may contain inaccurate medical facts, medication details, diagnoses, or treatment plans. <br>
Mitigation: Treat every output as an unverified draft and require licensed clinician review before entering content into patient records or using it for care decisions. <br>
Risk: JSON export may retain raw input and identifiers. <br>
Mitigation: Use JSON export only when retaining raw input and identifiers is acceptable under the applicable privacy and retention controls. <br>
Risk: Examples may resemble clinical treatment guidance. <br>
Mitigation: Do not use examples as treatment guidance or for psychiatric, diagnostic, or medication decisions without licensed clinician review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AIPOCH-AI/automated-soap-note-generator) <br>
- [Clinical Documentation Guidelines](references/clinical_guidelines.md) <br>
- [Medical Terminology Reference](references/medical_terminology.md) <br>
- [Sample SOAP Notes](references/sample_soap_notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, code, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON SOAP-note drafts, with supporting code examples and shell commands in the skill guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are draft clinical documentation and require licensed clinician review before use in patient records.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
