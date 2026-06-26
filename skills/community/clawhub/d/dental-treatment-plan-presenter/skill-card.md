## Description: <br>
Converts dentist-supplied comprehensive-exam findings into a draft phased, CDT-coded dental treatment plan with alternatives, risks, benefits, cost narrative prompts, and an informed-consent prompt sheet for licensed-dentist review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Dental professionals, supervised dental trainees, and treatment coordinators use this skill to turn clinical findings into a structured draft treatment-plan presentation. It supports phased care planning, CDT-code drafting, alternatives and risk prompts, and unresolved decision lists for review by the licensed dentist before patient presentation or treatment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Draft treatment plans may contain incorrect CDT codes, sequencing, clinical assumptions, fees, risks, or consent language. <br>
Mitigation: The licensed dentist must verify and edit all generated codes, sequencing, estimates, risks, and consent language before presentation or treatment. <br>
Risk: Unnecessary patient identifiers or protected health information could be included in user-provided case details. <br>
Mitigation: Use chart numbers or initials only, redact direct identifiers from drafts, and avoid entering unnecessary patient identifiers. <br>
Risk: Patients could mistake draft planning support for diagnosis, consent, or final treatment advice. <br>
Mitigation: Use the skill only with dental professionals or supervised staff, keep outputs marked DRAFT, and route patient-facing decisions through the licensed dentist. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown draft treatment plan with tables, phase sections, consent prompts, and unresolved decision lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are marked as drafts for licensed dentist review and avoid direct patient identifiers, final diagnoses, binding fees, final CDT coding, or signed consent.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
