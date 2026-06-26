## Description: <br>
Use when drafting patient discharge summaries, creating personalized discharge instructions, simulating post-discharge outcomes, reducing hospital readmissions, or optimizing care transitions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical documentation teams, care-transition staff, and agent developers use this skill to draft discharge summaries, patient-friendly instructions, follow-up plans, and readmission-risk-oriented care plans from patient and hospital-course inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes unsupported medical AI claims and can generate risk scores, medication reconciliation, follow-up timing, and patient instructions that may be clinically incorrect or misleading. <br>
Mitigation: Use outputs only as drafts for qualified clinician review; do not rely on generated clinical recommendations without validation against approved medical workflows. <br>
Risk: The skill handles patient discharge data and may involve protected health information. <br>
Mitigation: Use only in an approved clinical environment with secure PHI handling controls, access controls, and privacy review. <br>
Risk: Evidence security guidance advises non-production drafting or review use unless the skill is revised and validated. <br>
Mitigation: Limit deployment to review workflows until clinical validation, privacy controls, and operational guardrails are completed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/AIPOCH-AI/digital-twin-discharge-drafter) <br>
- [Discharge Summary Template](references/discharge_template.md) <br>
- [Medical Terms Reference](references/medical_terms.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell examples, plus structured discharge-summary and care-plan text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include patient-facing instructions, readmission-risk scores, medication lists, follow-up timing, and validation notes that require clinical review.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
