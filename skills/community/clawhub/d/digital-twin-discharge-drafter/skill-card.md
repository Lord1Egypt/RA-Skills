## Description:

Drafts AI-enhanced discharge summaries, personalized discharge instructions, post-discharge outcome simulations, and risk-based care plans using digital twin patient-model inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Healthcare teams, clinicians, and care-transition developers use this skill to draft discharge summaries, patient-facing instructions, scenario simulations, and risk-based post-discharge plans. The generated clinical content and prediction outputs require review in an approved clinical workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill claims to generate medical digital-twin predictions without evidence of real model validation.

Mitigation: Use predictions only as draft decision-support outputs after validation in the deployment environment and require clinician review before patient use.

Risk: The skill is intended for discharge workflows that may involve protected health information.

Mitigation: Run only in an approved clinical environment with PHI controls, access logging, and data handling policies appropriate for patient records.

Risk: The skill requests broader agent permissions than its documented behavior appears to need.

Mitigation: Constrain execution permissions, review file writes and shell usage, and pin or remove dependencies before installation.

## Reference(s):

- [Discharge Summary Template](artifact/references/discharge_template.md)
- [Medical Terms Reference](artifact/references/medical_terms.json)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/digital-twin-discharge-drafter)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured text with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include discharge-summary fields, patient-friendly instructions, readmission risk scores, scenario simulations, care-plan recommendations, and validation notes.]

## Skill Version(s):

0.1.0 (source: server release metadata and tile.json; SKILL.md metadata lists 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
