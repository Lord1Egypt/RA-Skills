## Description: <br>
Barefoot Doctor (EN) provides reference-only integrative medicine guidance for symptom triage, TCM pattern differentiation, Western differential framing, first aid, acupuncture, herbal medicine, and prevention. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnsmithfan](https://clawhub.ai/user/johnsmithfan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents can use this skill to structure reference-only responses about symptoms, TCM pattern differentiation, first aid triage, acupuncture, herbs, and prevention. It is intended to encourage emergency escalation and professional medical review rather than replace qualified care. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: High-stakes diagnosis, treatment, emergency, pediatric, herbal, and acupuncture guidance may be incorrect or unsafe if treated as medical care. <br>
Mitigation: Use the skill only as reference material and verify medical decisions with qualified local professionals. <br>
Risk: The artifact references 120 for emergencies, which may not be the user's local emergency number. <br>
Mitigation: Replace emergency-number guidance with the user's local emergency service number before relying on emergency instructions. <br>
Risk: Users may disclose identifying health details while seeking guidance. <br>
Mitigation: Avoid entering identifying health information and keep prompts limited to the minimum details needed for general reference guidance. <br>
Risk: Medication, herb, acupuncture, pregnancy, pediatric, and chronic disease guidance can carry patient-specific contraindications. <br>
Mitigation: Require review by qualified clinicians or pharmacists before acting on those recommendations. <br>


## Reference(s): <br>
- [Barefoot Doctor (EN) ClawHub release](https://clawhub.ai/johnsmithfan/barefoot-doctor) <br>
- [Method Patterns and Code Templates](references/method-patterns.md) <br>
- [Copy-Paste Prompt Templates](01-implement-method.md) <br>
- [Robustness and Safety Checklists](02-robustness-checks.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with optional JSON request and response structures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reference medical guidance only; no tools or external services are required by the artifact.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and target metadata; changelog v2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
