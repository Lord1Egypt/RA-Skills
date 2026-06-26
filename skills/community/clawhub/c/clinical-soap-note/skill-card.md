## Description: <br>
Use this skill when a clinician or medical scribe needs to convert raw encounter notes, dictation, or bullet points into a structured SOAP note. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinicians and medical scribes use this skill to turn raw encounter material into a concise SOAP note draft with missing-information flags, non-binding coding prompts, and a clinician-review notice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Patient information may be sensitive. <br>
Mitigation: Treat encounter content as PHI, avoid entering unnecessary identifiers, and do not store, transmit, or reuse encounter data beyond the current session. <br>
Risk: Generated notes may contain omissions or errors if used without review. <br>
Mitigation: Require a licensed clinician to verify, correct, and sign every draft before clinical, billing, or medical-record use. <br>
Risk: Coding prompts could be mistaken for final billing codes. <br>
Mitigation: Keep coding output as non-binding questions for coder review and never present final ICD-10 or CPT codes. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown SOAP note draft] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes gap flags, non-binding coding prompts, unresolved clinician-review items, and a mandatory review notice.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata and changelog, released 2026-05-28) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
